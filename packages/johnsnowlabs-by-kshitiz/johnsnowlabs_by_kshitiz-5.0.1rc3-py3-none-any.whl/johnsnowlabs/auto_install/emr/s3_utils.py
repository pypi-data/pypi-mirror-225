import boto3
import botocore

from johnsnowlabs.auto_install.emr.errors import BotoException


def create_emr_bucket(sts_client: boto3.client, s3_client: boto3.client, bucket_name):
    """Create a bucket for EMR cluster logs
    :param sts_client: STS client
    :param s3_client: S3 client
    :param bucket_name: Bucket name
    """
    try:
        account_id = sts_client.get_caller_identity()["Account"]
        if not bucket_name:
            bucket_name = f"johnsnowlabs-emr-{account_id}"

        s3_client.create_bucket(Bucket=bucket_name)
        return bucket_name
    except botocore.exceptions.ClientError as e:
        raise BotoException(
            code=e.response["Error"]["Code"], message=e.response["Error"]["Message"]
        )


def check_if_file_exists_in_s3(s3_client: boto3.client, s3_url: str):
    """Check if file exists in s3 using s3 client
    :param s3_client: S3 client
    :param s3_url: S3 url to check
    """
    try:
        s3_client.head_object(
            Bucket=s3_url.split("/")[2], Key="/".join(s3_url.split("/")[3:])
        )
        return True
    except botocore.exceptions.ClientError as e:
        return False
    except Exception:
        return False


def upload_file_to_s3(s3_client, file_path, bucket, file_name) -> str:
    """Upload a file to s3 bucket
    :param file_path: Path to file to upload
    :param bucket: Bucket to upload to
    :param file_name: File name to create
    :return s3_url: S3 url of uploaded file
    """
    try:
        s3_client.upload_file(file_path, bucket, file_name)
        return f"s3://{bucket}/{file_name}"
    except botocore.exceptions.ClientError as e:
        raise BotoException(
            code=e.response["Error"]["Code"], message=e.response["Error"]["Message"]
        )


def upload_content(s3_client, content, bucket, file_name):
    """Upload content to s3 bucket

    :param content: Content to upload
    :param bucket: Bucket to upload to
    :param file_name: File name to create
    :return: s3_url: S3 url of uploaded file
    """

    try:
        s3_client.put_object(Body=content, Bucket=bucket, Key=file_name)
        return f"s3://{bucket}/{file_name}"
    except botocore.exceptions.ClientError as e:
        raise BotoException(
            code=e.response["Error"]["Code"], message=e.response["Error"]["Message"]
        )
