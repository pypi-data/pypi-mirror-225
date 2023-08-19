# psusannx_s3

A package that allows a connection to the Amazon simple storage service ([S3](https://aws.amazon.com/s3/)) to be made, provided a valid set of AWS credentials are provided. This connection is set up through a python class which, once created, can allow for easy read/write functions for certain file extensions (.csv, .json, .pkl, .h5). It uses the boto3 package to perform these actions.
The docs for using boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

This package was created to be used as a subpackage in a wider project - PSUSANNX.

## Package classes

- PsusannxS3

## Installation

```python
pip install psusannx-s3
```

## Usage

```python
# Import the function from the package
from psusannx_s3 import PsusannxS3

# Get some info about the function
help(PsusannxS3) 
```

Set up a connection to the S3 service by instantiating the class with valid credentials. And store that connection in a variable `s3`. 

```python
# Store the AWS credentials as variables
AWS_ACCESS_KEY = "<aws-access-key>"
AWS_SECRET_KEY = "<aws-secret-key>"

# Set up the connection to AWS s3 through the PsusannxS3 class
s3 = PsusannxS3(
    aws_access_key=AWS_ACCESS_KEY, 
    aws_secret_key=AWS_SECRET_KEY
)
```

Now that we have created a connection to the S3 service with the credentials provided, we can use the class to read/write files to S3. We will demonstrate this with a pickled list object but the same steps & syntax apply for each of the other file types. **For this step to work, you need to set up an AWS account & have a bucket created in S3 in your account (and that the credentials provided above have the required permissions to read/write to the S3 service)**.

```python
# Create a listthat we want to put in S3
test_list = [1, 2, 3]

# Use the s3 instance of the class to put the list in S3
s3.write_pkl_to_s3(
    bucket_name="<s3-bucket-name>",
    object_name="<path\to\file\in\bucket\file_name.pkl>",
    data=test_list
)
```

We can now read the same file/list from the S3 bucket into the code, and even save the file to the local directory if necessary.

```python
# Read the pickled list from S3 to the test_list variable 
# & aslo persist the file to the current directory using retain=True
test_list = s3.read_pkl_from_s3(
    bucket_name="<s3-bucket-name>",
    object_name="<path\to\file\in\bucket\file_name.pkl>",
    retain=True
)

# Print the list to screen
print(test_list)
```

## Notes

- The package is quite restricted in what it can do, but it only needs to do things that are required by the parent project so there won't be much development.
