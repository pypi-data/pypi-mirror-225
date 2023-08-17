import sys
import os
import boto3
import mimetypes

from .config import *
from awyes import awyes
from pathlib import Path
from botocore.exceptions import ClientError


def init(bucket_name):
    """
    Initialize your S3 bucket

    :param bucket_name: Name of your aws bucket
    :return: None
    """
    write_config_to_file(bucket_name)

    print(Path(__file__))
    print(Path(__file__).parent)

    awyes_template = (Path(__file__).parent / "awyes_template.yml").resolve()

    with open(awyes_template, 'r') as file:
        awyes_yaml = file.read().replace('${BUCKET_NAME}', bucket_name)

    awyes.Deployment(config=awyes_yaml).deploy()


def upload_file(file_name, object_name):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: url, or error
    """
    bucket_name = read_config_from_file().strip()

    # If S3 object_name was not specified, use file_name
    if not object_name:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        content_type, _ = mimetypes.guess_type(file_name)

        s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={
                              'ContentType': content_type})

        location = s3_client.get_bucket_location(Bucket=bucket_name)[
            'LocationConstraint']

        return f"https://s3-{location}.amazonaws.com/{bucket_name}/{object_name}"
    except ClientError as e:
        return e


def main():
    _, command, resource_name, *secondary_name = sys.argv

    if command.lower() == 'init':
        init(bucket_name=resource_name)
    elif command.lower() == 'upload':
        secondary_name = secondary_name[0] if secondary_name else ""
        url = upload_file(file_name=resource_name, object_name=secondary_name)
        print(url)


if __name__ == '__main__':
    main()
