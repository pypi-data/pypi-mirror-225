"""The class that will serve as a connection to AWS S3 service for PSUSANNX project"""

# Import packages
import pandas as pd
import pickle as pkl
import json
import boto3
from tensorflow.keras.models import load_model
import os


class PsusannxS3():
    """A class containing functions for connecting to AWS S3 service."""

    def __init__(self, aws_access_key=None, aws_secret_key=None):
        """
        Use the AWS credentials to set up a connection to 
        an S3 bucket, through the boto3 s3 client, 
        on creation of the class instance.

        Parameters
        ----------
        aws_access_key: str
            The access key associated with the account you want to use to connect to s3.

        aws_secret_key: str
            The secret key associated with the account you want to use to connect to s3.
        """

        # If no credentials are passed then print a quick message
        if (aws_access_key is None) or (aws_secret_key is None):
            print("If you want to access private S3 buckets, you will need to provide valid AWS secret & access keys.\nOtherwise you can only access public buckets.")
        
         # Create a new S3 client    
        self.s3_client = boto3.client(
            service_name="s3", 
            region_name="eu-west-1",
            aws_secret_access_key=aws_secret_key, 
            aws_access_key_id=aws_access_key
        )


    def download_file(self, bucket_name: str, s3_filepath: str, local_filepath: str):
        """
        Download a file from s3 onto the local machine.

        Parameters
        ----------
        bucket_name: str
            The name of the s3 bucket that we want to download the file from.

        s3_filepath: str
            The path to the file that we want to download from s3 (from within the bucket).

        local_filepath: str
            The path that we want to store the file to on the local machine.

        Returns
        -------
        None
        """

        # Download the file from the s3 bucket & put it on the local machine
        self.s3_client.download_file(
            Bucket=bucket_name, 
            Key=s3_filepath, 
            Filename=local_filepath
        )


    def upload_file(self, bucket_name: str, s3_filepath: str, local_filepath: str):
        """
        Upload a file to s3 from the local machine. 
        Using the s3 boto client that was set up on instantiation.

        Parameters
        ----------
        bucket_name: str
            The name of the s3 bucket that we want to upload the file to.

        s3_filepath: str
            The path to the file that we want the uploaded file to be on s3 (within the bucket).

        local_filepath: str
            The path of the file on the local machine that we want to upload..

        Returns
        -------
        None
        """

        # Upload the file to the s3 bucket from the local machine
        self.s3_client.upload_file(
            Bucket=bucket_name, 
            Key=s3_filepath, 
            Filename=local_filepath
        )


    # CSV
    def read_csv_from_s3(self, bucket_name: str, object_name: str, retain=False):
        """
        Read a csv file from s3 as a pandas DataFrame.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be read from.

        object_name: str
            The path to the object within the bucket. eg "folder/subfolder/file.csv"

        retain: bool
            If True, the csv file that is downloaded from s3 will not be deleted after the 
            data has been read in as an object.
        
        Returns
        -------
        Pandas DataFrame object.
        """

        # Download the csv file from s3 onto the local machine
        self.download_file(bucket_name=bucket_name, s3_filepath=object_name, local_filepath=object_name)
        
        # Read in the csv as a pandas dataframe
        data = pd.read_csv(object_name)

        # Delete the file from the local machine to remove clutter
        if not retain:
            os.remove(object_name)

        return data


    def write_csv_to_s3(self, bucket_name: str, object_name: str, data: pd.DataFrame):
        """
        Write a pandas DataFrame to a csv in s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to the object within the bucket. eg "folder/subfolder/file.csv"
        
        data: pandas.DataFrame
            The dataframe object to be saved to a csv.

        Returns
        -------
        None
        """

        # First of all write the csv to a file on the local machine
        data.to_csv(object_name, index=False)

        # Upload the file to s3 from the local machine
        self.upload_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Delete the file once it has been uploaded to s3
        os.remove(object_name)

        return None
        

    # JSON
    def read_json_from_s3(self, bucket_name: str, object_name: str, retain=False):
        """
        Read a json file from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to the json file within the bucket. eg "folder/subfolder/file.json"

        retain: bool
            If True, the json file that is downloaded from s3 will not be deleted after the 
            data has been read in as an object.

        Returns
        -------
        A python dictionary.
        """

        # Download the file from s3 onto the local machine
        self.download_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Open the file & read in the data as a dictionary
        with open(object_name, 'rb') as f:
            data = json.load(f)

        # Delete the file from the local machine to remove clutter
        if not retain:
            os.remove(object_name)

        return data
    
    
    def write_json_to_s3(self, bucket_name: str, object_name: str, data: dict):
        """
        Write a json file to s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to put the json file within the bucket. eg "folder/subfolder/file.json"

        data: dict
            The data to be put into s3.

        Returns
        -------
        None
        """
        
        # Write the json dictionary to a json file on the local machine
        with open(object_name, "w") as f:
            json.dump(data, f)

        # Upload the file to s3 from the local machine
        self.upload_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Delete the file from the local machine once it has been uploaded to s3
        os.remove(object_name)

        
    # H5
    def read_h5_from_s3(self, bucket_name: str, object_name: str, retain=False):
        """
        Read a h5 model object from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the model object should be read from.

        object_name: str
            The path to the .h5 model object file within the bucket. eg "folder/subfolder/model_name.h5"

        retain: bool
            If True, the json file that is downloaded from s3 will not be deleted after the 
            data has been read in as an object.
        
        Returns
        -------
        A keras model object.
        """

        # Download the file from s3 to the local machine
        self.download_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Read in the model that has been downloaded from s3
        data = load_model(object_name)

        # Delete the file from the local machine to remove clutter
        if not retain:
            os.remove(object_name)

        return data
    

    def write_h5_to_s3(self, bucket_name: str, object_name: str, data):
        """
        Write a keras model object (.h5 extension) to s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to put the file within the s3 bucket. eg "folder/subfolder/h5_file.h5"

        data: keras model object
            A trained keras model object.
        
        Returns
        -------
        None
        """

        # First save the model to the local directory, to be copied to s3
        data.save(object_name)

        # Put the model into the s3 bucket
        self.upload_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )
        
        # Remove the model object file from the local directory
        os.remove(object_name)


    # PKL
    def read_pkl_from_s3(self, bucket_name: str, object_name: str, retain=False):
        """
        Read a pickled object (.pkl extension) from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the .pkl file should be read from.

        object_name: str
            The path to .pkl object within the bucket. eg "folder/subfolder/file.pkl"

        retain: bool
            If True, the json file that is downloaded from s3 will not be deleted after the 
            data has been read in as an object.
        
        Returns
        -------
        An unpickled object to be used
        """

        # Download the file from s3 to the local machine
        self.download_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Open the pkl file & read in the data as a python object
        with open(object_name, "rb") as f:
            data = pkl.load(f)
        
        # Delete the file from the local machine to remove clutter
        if not retain:
            os.remove(object_name)

        return data
    

    def write_pkl_to_s3(self, bucket_name: str, object_name: str, data):
        """
        Write an object that can be pickled (.pkl extension) like a python list, to s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the object should be written to.

        object_name: str
            The path to the json file within the bucket. eg "folder/subfolder/object.pkl"

        data: a python object that can be pickled. eg a python list.
        
        Returns
        -------
        None
        """

        # First pickle the object to a file on the local machine
        with open(object_name, "wb") as f:
            pkl.dump(data, f)

        # Upload the file to s3 from the local machine
        self.upload_file(
            bucket_name=bucket_name, 
            s3_filepath=object_name, 
            local_filepath=object_name
        )

        # Delete the file from the local machine once it has been uploaded to s3
        os.remove(object_name)


    