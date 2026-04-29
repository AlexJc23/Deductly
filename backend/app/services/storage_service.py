from app.core.config import settings
from fastapi import UploadFile, HTTPException
from typing import Optional
import boto3
import uuid




def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=settings.aws_region
    )

def upload_file_to_s3(file: UploadFile, user_id: int) -> str:
    s3_client = get_s3_client()
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}/{uuid.uuid4()}.{file_extension}"

    try:
        s3_client.upload_fileobj(
            file.file,
            settings.s3_bucket,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    file_url = f"https://{settings.s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{unique_filename}"
    return file_url

def delete_file_from_s3(file_url: str):
    s3_client = get_s3_client()
    bucket_name = settings.s3_bucket
    key = file_url.split(f"https://{bucket_name}.s3.{settings.aws_region}.amazonaws.com/")[-1]

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
