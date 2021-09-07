import logging

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from decouple import config
from fastapi import UploadFile

from app.utils.date_utils import D


class S3:
    s3_client: BaseClient = boto3.client(
        service_name="s3",
        aws_access_key_id=config("AWS_ACCESS_KEY"),
        aws_secret_access_key=config("AWS_SECRET_KEY")
    )
    BUCKET_NAME = "fleapto-files"
    url = "https://{bucket}.s3.ap-northeast-2.amazonaws.com/{filename}"

    @classmethod
    def upload_file_to_bucket(cls, file: UploadFile):
        filename = f"{D.datetimenum()}_{file.filename}"
        try:
            response = cls.s3_client.upload_fileobj(
                file.file,
                cls.BUCKET_NAME,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
        except ClientError as e:
            logging.error(e)
            return None

        url = cls.url.format(bucket=cls.BUCKET_NAME, filename=filename)
        return url