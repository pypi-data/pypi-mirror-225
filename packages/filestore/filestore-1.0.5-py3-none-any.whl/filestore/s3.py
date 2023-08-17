"""
Amazon S3 storage for FastAPI. This module contains the S3Storage class which is used to upload files to Amazon S3.
"""
import os
import asyncio
import logging
from typing import BinaryIO, List
from urllib.parse import quote as urlencode
from logging import getLogger

logger = getLogger(__name__)

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError as err:
    logger.warning('boto3 is not installed. S3Storage will not be available.')
    raise err

try:
    from functools import cache
except ImportError:
    from functools import lru_cache

    cache = lru_cache(maxsize=None)

from .main import FastStore, FileData, UploadFile, FileField

logger = logging.getLogger(__name__)


class S3Storage(FastStore):
    """
    Amazon S3 storage for FastAPI.

    Properties:
        client (boto3.client): The S3 client.
    """

    @property
    @cache
    def client(self):
        """
        Get the S3 client. Make sure the AWS credentials are set in the environment variables.
        This property is cached.

        Returns:
            boto3.client: The S3 client.
        """
        key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region_name = os.environ.get('AWS_DEFAULT_REGION') or self.config.get('region')
        return boto3.client('s3', region_name=region_name, aws_access_key_id=key_id, aws_secret_access_key=access_key)

    async def _upload(self, *, file_obj: BinaryIO, bucket: str, obj_name: str, extra_args: dict):
        """
        Private method to upload the file to the destination. This method is called by the upload method.

        Args:
            file_obj (BinaryIO): The file object to upload.
            bucket (str): The name of the bucket to upload the file to.
            obj_name (str): The name of the object.
            extra_args (dict): Extra arguments to pass to the upload_fileobj method.

        Returns:
            None: Nothing is returned.
        """
        try:
            await asyncio.to_thread(self.client.upload_fileobj, file_obj, bucket, obj_name, ExtraArgs=extra_args)
        except AttributeError:
            self.client.upload_fileobj(file_obj, bucket, obj_name, ExtraArgs=extra_args)

    # noinspection PyTypeChecker
    async def upload(self, *, file_field: FileField):
        """
        Upload a file to the destination the S3 bucket.

        Args:
            file_field (tuple[str, UploadFile]): A tuple containing the field name and the UploadFile object.

        Returns:
            None: Nothing is returned.
        """
        field_name, file = file_field['name'], file_field['file']
        try:
            dest = file_field.get('config', {}).get('destination') or self.config.get('destination', None)
            object_name = dest(self.request, self.form, field_name, file) if dest else file.filename
            bucket = file_field.get('config', {}).get('bucket') or self.config.get('bucket') or os.environ.get(
                'AWS_BUCKET_NAME')
            region = self.config.get('region') or os.environ.get('AWS_DEFAULT_REGION')
            extra_args = file_field.get('config', {}).get('extra_args', {}) or self.config.get('extra_args', {})

            if file_field.get('config', {}).get('background') or self.config.get('background', False):
                self.background_tasks.add_task(self._upload, file_obj=file.file, bucket=bucket, obj_name=object_name,
                                               extra_args=extra_args)
            else:
                await self._upload(file_obj=file.file, bucket=bucket, obj_name=object_name, extra_args=extra_args)

            url = f"https://{bucket}.s3.{region}.amazonaws.com/{urlencode(object_name.encode('utf8'))}"
            self.store = FileData(filename=file.filename, content_type=file.content_type, field_name=field_name,
                                  url=url, message=f'{file.filename} successfully uploaded')
        except(NoCredentialsError, ClientError, AttributeError, ValueError, NameError, TypeError) as err:
            logger.error(f'Error uploading file: {err} in {self.__class__.__name__}')
            self.store = FileData(status=False, error=str(err), field_name=field_name, filename=file.filename,
                                  message=f'Unable to upload {file.filename}')

    async def multi_upload(self, *, file_fields: List[FileField]):
        """
        Upload multiple files to the destination S3 bucket.
        Since the upload method is a coroutine, we can use asyncio.gather to upload multiple files concurrently.

        Args:
            file_fields (list[FileField]): A of FileField objects.

        Returns:
            None: Nothing is returned.
        """
        await asyncio.gather(*[self.upload(file_field=file_field) for file_field in file_fields])
