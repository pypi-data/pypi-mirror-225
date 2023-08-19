from setuptools import setup, find_packages
from pathlib import Path

# Get the current directory of the setup.py file (as this is where the README.md will be too)
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

# Set up the package metadata
setup(
    name="psusannx_s3",
    author="Jamie O'Brien",
    description="A package for reading/writing certain file types to the AWS S3 service using boto3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    packages=find_packages(include=["psusannx_s3", "psusannx_s3.*"]),
    install_requires=[
        "boto3>=1.24.51",
        "pandas>=1.3.4",
        "tensorflow>=2.13.0"
    ],
    project_urls={
        "Source Code": "https://github.com/jamieob63/psusannx_s3.git",
        "Bug Tracker": "https://github.com/jamieob63/psusannx_s3.git/issues",
    }
)