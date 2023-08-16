# imports
import boto3
import datetime


class s3Upload:
    """
    This class is to facilitate the interation with s3 buckets (aws or other)

    Attributes
    ----------
    access_key : str
        the access key of the bucket (this must be generated or give to you by the bucket admin)
    secret_key : str
        the secret key of the bucket (this must be generated or give to you by the bucket admin)
    bucket_name : str
        the bucket name of the bucket itself
    verify_ssl: bool
        verify the ssl certificate of the endpoint of the bucket
    bucket_endpoint
        the endpoint of the bucket, use if needed (for aws is not needed)
    region_name
        the region name of the bucket, use if needed (you can ask the admin of the bucket)
    """

    def __init__(self, access_key: str, secret_key: str, bucket_name: str, verify_ssl=True, bucket_endpoint=None, region_name=None):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__bucket_name = bucket_name
        self.__bucket_endpoint = bucket_endpoint
        self.__region_name = region_name
        self.__date = None
        self.__time = None
        self.__s3_bucket = None
        self.__verify = verify_ssl

    def create_bucket_conn(self):
        """Create the connection to the s3 bucket"""

        if self.__bucket_endpoint is None and self.__region_name is not None:
            self.__log(text_to_write="Create connection without bucket endpoint")
            self.__s3_bucket = boto3.client("s3", aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, region_name=self.__region_name)
        elif self.__region_name is None and self.__bucket_endpoint is not None:
            self.__log(text_to_write="Create connection without region name")
            self.__s3_bucket = boto3.client("s3", aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, endpoint_url=self.__bucket_endpoint)
        elif self.__region_name is not None and self.__bucket_endpoint is not None and not self.__verify:
            self.__log(text_to_write="Create connection to s3 bucket and with verify=False")
            self.__s3_bucket = boto3.client("s3", aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, endpoint_url=self.__bucket_endpoint, region_name=self.__region_name, verify=self.__verify)
        elif self.__region_name is None and self.__bucket_endpoint is not None and not self.__verify:
            self.__log(text_to_write="Create connection without region name and with verify=False")
            self.__s3_bucket = boto3.client("s3", aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, endpoint_url=self.__bucket_endpoint, verify=self.__verify)
        else:
            self.__log(text_to_write="Create connection to s3 bucket")
            self.__s3_bucket = boto3.client("s3", aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, endpoint_url=self.__bucket_endpoint, region_name=self.__region_name)

    def upload_object(self, bucket_object):
        """
        Using the connection created, this method will upload the bucket_object to the s3 bucket

        :param str bucket_object: file to upload
        """

        file = bucket_object
        self.__log(text_to_write=f"Upload file {file} to bucket")
        self.__s3_bucket.upload_file(file, self.__bucket_name, file)

    def verify_bucket(self, bucket_object):
        """
        Verify in the bucket the file requested

        :param str bucket_object: file to verify
        """

        for item in self.__s3_bucket.list_objects(Bucket=self.__bucket_name)['Contents']:
            if bucket_object in item['Key']:
                self.__log(text_to_write=f"Bucket object: {item['Key']}")

    def __log(self, text_to_write):
        """
        Print to the console the text passed through the parameter text_to_write

        :param text_to_write:
        """

        self.__date = datetime.date.today().strftime("%d/%m/%Y")
        self.__time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{self.__date} - {self.__time}] - {text_to_write}")
