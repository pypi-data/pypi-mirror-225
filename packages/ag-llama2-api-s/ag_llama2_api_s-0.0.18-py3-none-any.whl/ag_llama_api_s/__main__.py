"""
LLAMA API server.
"""
import json
import traceback
import secrets
import time
import sys

from loguru import logger
logger.remove(None)
logger.add("logs/{time:YYYY-MM-DD}.log",level = 'DEBUG', format = "{time:YYYY-MM-DD HH:mm:ss} | {level:<8} |{line:<3}|{file:<25} | {message}",rotation="10 MB")
loguru_format = "<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>|<level>{level:<8}|{file:<25}|{line:<3}></level>{message}"
logger.add(sys.stdout,level = 'DEBUG', format = loguru_format)
logger.level("INFO", color="<green>")

import waitress
from flask import Flask, Response, abort, jsonify, render_template, request
from flask_cors import CORS

from . import is_true
from .choice import reduce_choice
from .model import load_model

# Configurations from environment variables.
from . import MODEL
from . import HOST
from . import PORT
from . import MODEL_REVISION
from . import MODEL_CACHE_DIR
from . import MODEL_LOAD_IN_8BIT
from . import MODEL_LOAD_IN_4BIT
from . import MODEL_LOCAL_FILES_ONLY
from . import MODEL_TRUST_REMOTE_CODE
from . import MODEL_HALF_PRECISION
from . import SERVER_THREADS
from . import SERVER_IDENTITY
from . import SERVER_CONNECTION_LIMIT
from . import SERVER_CHANNEL_TIMEOUT
from . import SERVER_MODEL_NAME
from . import SERVER_NO_PLAYGROUND
from . import SERVER_CORS_ORIGINS
from . import COMPLETION_MAX_PROMPT
from . import COMPLETION_MAX_TOKENS
from . import COMPLETION_MAX_N
from . import COMPLETION_MAX_LOGPROBS
from . import COMPLETION_MAX_INTERVAL

keep_running_localy = True
# Load the language model to be served.
stream_model = None
def load_stream_model():
    global stream_model
    stream_model = load_model(
        name_or_path=MODEL,
        load_in_8bit=MODEL_LOAD_IN_8BIT,
        load_in_4bit=MODEL_LOAD_IN_4BIT,
    )
    logger.info(f"Model loaded")

# Create and configure application.
app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.json.compact = True
app.url_map.strict_slashes = False

# Configure cross-origin resource sharing (CORS).
CORS(app, origins=SERVER_CORS_ORIGINS.split(","))


def parse_options(schema):
    """Parse options specified in query parameters and request body."""
    options = {}
    payload = request.get_json(force=True, silent=True)
    for key, dtype in schema.items():
        # Allow casting from int to float.
        if dtype == float:
            dtypes = (int, float)
        else:
            dtypes = (dtype,)

        # Use custom function to convert string to bool correctly.
        if dtype == bool:
            dtype_fn = is_true
        else:
            dtype_fn = dtype

        # If an option appears in both the query parameters and the request
        # body, the former takes precedence.
        if key in request.args:
            options[key] = request.args.get(key, dtype(), type=dtype_fn)
        elif (
            isinstance(payload, dict)
            and key in payload
            and isinstance(payload[key], dtypes)
        ):
            options[key] = dtype(payload[key])

        # Temporary workaround for multiple prompts (#198).
        if (
            key == "prompt"
            and isinstance(payload, dict)
            and key in payload
            and isinstance(payload[key], list)
        ):
            prompts = payload[key]
            if len(prompts) == 1:
                options[key] = prompts[0]
            elif len(prompts) > 1:
                abort(400, description="only one prompt is supported")

    return options




@app.route("/v1/models")
def list_models():
    """List the currently available models."""
    info = {"id": SERVER_MODEL_NAME, "object": "model"}
    return jsonify(data=[info], object="list")


@app.route("/v1/models/<path:name>")
def retrieve_model(name):
    """Retrieve basic information about the model."""
    if name != SERVER_MODEL_NAME:
        abort(404, description="model does not exist")
    return jsonify(id=SERVER_MODEL_NAME, object="model")

@app.route("/alive", methods=["GET"])
def alive():
    return jsonify(alive=True)

@app.route("/v1/completions", methods=["GET", "POST"])
def create_completion():
    """Create a completion for the provided prompt and parameters."""
    schema = {
        "prompt": str,
        "min_tokens": int,
        "max_tokens": int,
        "temperature": float,
        "top_p": float,
        "n": int,
        "stream": bool,
        "logprobs": int,
        "echo": bool,
    }
    options = parse_options(schema)
    if "prompt" not in options:
        logger.warning("prompt not specified")
        options["prompt"] = ""

    
    # Limit maximum resource usage.
    # if len(options["prompt"]) > COMPLETION_MAX_PROMPT:
    #     logger.warning("prompt truncated to {} chars from {}", COMPLETION_MAX_PROMPT, len(options["prompt"]))
    #     options["prompt"] = options["prompt"][:COMPLETION_MAX_PROMPT]
    if options.get("min_tokens", 0) > COMPLETION_MAX_TOKENS:
        options["min_tokens"] = COMPLETION_MAX_TOKENS
    if options.get("max_tokens", 0) > COMPLETION_MAX_TOKENS:
        options["max_tokens"] = COMPLETION_MAX_TOKENS
    if options.get("n", 0) > COMPLETION_MAX_N:
        options["n"] = COMPLETION_MAX_N
    if options.get("logprobs", 0) > COMPLETION_MAX_LOGPROBS:
        options["logprobs"] = COMPLETION_MAX_LOGPROBS

    logger.debug("options: {}", options)
    try:
        # Return in event stream or plain JSON.
        logger.info("Generating completion")
        res=stream_model(options["prompt"],max_tokens=options["max_tokens"],temperature=options["temperature"],top_p=options["top_p"])
        logger.info(f"Completion generated:{res}")
        return jsonify(res)
        
    except Exception as e:
        logger.exception(traceback.TracebackException.from_exception(e))
        logger.error(f"Error generating completion: {e}", exc_info=True)
        abort(500, description=str(e))


def create_completion_json(options, template):
    """Return text completion results in plain JSON."""

    # Tokenize the prompt beforehand to count token usage.
    logger.info("Tokenizing prompt")
    options["prompt"] = stream_model.tokenize(options["prompt"],trim_to=COMPLETION_MAX_PROMPT)
    prompt_tokens = stream_model.get_tokens_count(options["prompt"])
    completion_tokens = 0

    # Add data to the corresponding buffer according to the index.
    buffers = {}
    for choice in stream_model(**options):
        completion_tokens += 1
        index = choice["index"]
        if index not in buffers:
            buffers[index] = []
        buffers[index].append(choice)

    #clear options to save memory
    options.clear()

    # Merge choices with the same index.
    data = template.copy()
    for _, buffer in buffers.items():
        if buffer:
            data["choices"].append(reduce_choice(buffer))

    # Include token usage info.
    data["usage"] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }

    return jsonify(data)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def http_error_handler(error):
    """Handler function for all expected HTTP errors."""
    logger.error(f"{error.code} {error.description}")
    return jsonify(error={"message": error.description}), error.code

def run_localy(ip,port,model,in8bit=False):
    global stream_model, keep_running_localy
    stream_model = load_model(
        name_or_path=model,
        load_in_8bit=in8bit,
        load_in_4bit=False,
    )
    while keep_running_localy:
        try:
            logger.info(f"Starting API...")
            logger.info(f"Start listening on {HOST}:{PORT}")
            waitress.serve(
                app,
                host=ip,
                port=port,
                threads=SERVER_THREADS,
                ident=SERVER_IDENTITY,
                connection_limit=SERVER_CONNECTION_LIMIT,
                channel_timeout=SERVER_CHANNEL_TIMEOUT,
            )
            logger.info(f"API stopped")
        except Exception as e:
            logger.exception(traceback.TracebackException.from_exception(e))
            logger.error(f"Error generating completion: {e}", exc_info=True)
            logger.info(f"Waiting 2 minutes before retrying starting up AI API...")
            time.sleep(2*60)



def main():
    """Start serving API requests."""
    load_stream_model()
    logger.info(f"start listening on {HOST}:{PORT}")
    waitress.serve(
        app,
        host=HOST,
        port=PORT,
        threads=SERVER_THREADS,
        ident=SERVER_IDENTITY,
        connection_limit=SERVER_CONNECTION_LIMIT,
        channel_timeout=SERVER_CHANNEL_TIMEOUT,
    )


if __name__ == "__main__":
    logger.info(f"Running from __main__")
    main()
