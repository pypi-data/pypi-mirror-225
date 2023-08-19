import setuptools
import re 
import os

version="0.0.4"

def find_latest_version(folder_path):
    version_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
    latest_version = None

    for file_name in os.listdir(folder_path):
        match = version_pattern.search(file_name)
        if match:
            version = tuple(int(match.group(i)) for i in range(1, 4))
            if latest_version is None or version > latest_version:
                latest_version = version

    return latest_version

def get_next_version(current_version):
    major, minor, patch = current_version
    next_version = (major, minor, patch + 1)
    return next_version

V= find_latest_version('dist')
if V is not None:
    V = get_next_version(V)
    version = '.'.join(str(i) for i in V)
else:
    print('No version found')

print('Version: ', version)

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="ag_llama2_api_s",                     # This is the name of the package
    version=version,                        # The initial release version
    author="AA",                     # Full name of the author
    description="ag_llama2_api_s Test Package for Somthing",
    long_description="long_description",      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages= setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    scripts=["utils/download.py", "utils/render.py"],
    include_package_data=True,                                     # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    # py_modules=["ag_llama_api"],             # Name of the python package
    # package_dir={'':'src'},     # Directory of the source code of the package
    install_requires=required                     # Install other dependencies if any
)