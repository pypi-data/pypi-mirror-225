"""
A text generation model with stream decoding.
"""
import gc
import pynvml
import torch
from sentencepiece import SentencePieceProcessor

from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline
from loguru import logger



class StreamModel:
    """StreamModel wraps around a language model to provide stream decoding."""

    def __init__(self, model, tokenizer,**kwargs):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        
        self.path=kwargs.get('path',None)
        if self.path:
            self.s_tokenizer =SentencePieceProcessor(model_file=f"{self.path}/tokenizer.model")

    def __call__(
        self,
        prompt,
        max_tokens=16,
        temperature=1.0,
        top_p=1.0,
    ):
        self.wait_and_clear_gpu()
        logger.info(f"Got number of tokens: {self.get_tokens_count(prompt)}")
        """Create a completion stream for the provided prompt."""
        logger.info(f"Generating pipeline for {self.path}")
        pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=max_tokens,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=1.15
            )
        logger.info(f"Pipeline generated")
        logger.info(f"Generating text for {self.path}")
        raw_output = pipe(prompt)
        logger.info(f"Text generated")
        text = raw_output[0]["generated_text"]  
        return text
        
    

    def tokenize(self, text,trim_to=2048):
        """Tokenize a string into a tensor of token IDs."""
        num_tokens = self.get_tokens_count(text)            
        if num_tokens>trim_to:
            raise ValueError(f"Tokenized original text:{num_tokens} tokens, trimed:{trim_to} tokens. Some tokens are lost, please try to reduce the length of the input text.")
        self.wait_and_clear_gpu()
        with torch.inference_mode():
            batch = self.tokenizer.encode(text,truncation=True,max_length=trim_to,return_tensors="pt")
            logger.debug(f"Sending tokenized text to device {self.device}")
            res=batch[0].to(self.device)
        logger.debug(f"Tokenized original text:{num_tokens} tokens, trimed:{batch.shape[-1]} tokens")
        
        return res

    
    
    def get_tokens_count(self, prompt):
        """Tokenize a string into a tensor of token IDs."""
        if isinstance(prompt, str):
            if len(prompt) == 0:
                return 0
            if self.s_tokenizer:
                return len(self.s_tokenizer.EncodeAsIds(prompt))+1#+1 for eos
            batch = self.tokenizer.encode(prompt, return_tensors="pt")
            return batch.shape[-1]
        elif isinstance(prompt, torch.Tensor) and prompt.dim() == 1:
            return prompt.shape[-1]
        raise TypeError("prompt must be a string or a 1-d tensor")
    
    

    def wait_and_clear_gpu(self):
        """Wait for GPU memory to be released and clear the cache."""
        # torch.cuda.empty_cache()
        logger.debug("Waiting for GPU memory to be released")
        
        pynvml.nvmlInit()
        gpus_count = pynvml.nvmlDeviceGetCount()
        logger.debug(f"Found {gpus_count} GPUs")
        handles = []
        for index in range(gpus_count):
            try:
                handles.append(pynvml.nvmlDeviceGetHandleByIndex(index))
                logger.debug(f"Got handle for GPU {index}")
            except Exception as e:
                logger.error(f"Failed to get handle for GPU {index}: {e}")
        
        for i,handle in enumerate(handles):
            info=pynvml.nvmlDeviceGetMemoryInfo(handle)
            logger.debug(f"GPU {i} memory info: {gpu_sum(info)}") 
        
        # logger.debug(torch.cuda.memory_stats())
        
        logger.debug("Clearing GPU cache")
        gc.collect()
        torch.cuda.empty_cache()
        gc.collect()

        for i,handle in enumerate(handles):
            info=pynvml.nvmlDeviceGetMemoryInfo(handle)
            logger.debug(f"GPU {i} memory info: {gpu_sum(info)}") 

        # logger.debug(torch.cuda.memory_stats())
        
        pynvml.nvmlShutdown()
        

def load_model(
    name_or_path,
    load_in_8bit=False,
    load_in_4bit=False,
):
    """Load a text generation model and make it stream-able."""
    logger.info(f"Loading tokenizer from {name_or_path}")
    tokenizer = LlamaTokenizer.from_pretrained(name_or_path)
    logger.info(f"Tokenizer loaded")
    logger.info(f"Loading model from {name_or_path}")
    model = LlamaForCausalLM.from_pretrained(name_or_path, device_map="auto", load_in_8bit=load_in_8bit)
    logger.info(f"Model loaded")
    # Check if the model has text generation capabilities.
    if not model.can_generate():
        logger.error(f"{name_or_path} is not a text generation model")
        raise TypeError(f"{name_or_path} is not a text generation model")

    return StreamModel(model, tokenizer,path=name_or_path)

def gpu_sum(info):
    bytes_gib = 1024.0 ** 3
    s=""        
    s+='used:'+f"{int(info.used / bytes_gib)} GiB | "
    s+='free:'+ f"{int(info.free / bytes_gib)} GiB | "
    s+='total:'+f"{int(info.total / bytes_gib)} GiB |"
    return s