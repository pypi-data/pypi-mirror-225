from google.cloud import storage
import gcshus
import boto3
import dataclasses


class UnsupportedService(Exception):
    pass


class UnsupportedOperation(Exception):
    pass


class NotServiceAccountException(Exception):
    pass


@dataclasses.dataclass
class UploadResult:
    url: str


class Client:
    def __init__(self, service) -> None:
        if service.lower() == "gcs":
            self.storage_service = GCS()
            return

        if service.lower() == "s3":
            self.storage_service = S3()
            return

        raise UnsupportedService(f"Unsupported service: {service}")

    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        return self.storage_service.upload(bucket, src_file, dst_file)

    def generate_download_url(self, bucket, file, mins) -> str:
        return self.storage_service.generate_download_url(bucket, file, mins)


class StorageService:
    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        raise UnsupportedOperation("Upload operation is not supported")

    def generate_download_url(self, bucket, file, mins) -> str:
        raise UnsupportedOperation("Download URL generation is not supported")


class GCS(StorageService):
    def __init__(self) -> None:
        self.gcs_client = storage.Client()

    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        gcshus.upload(self.gcs_client, bucket, src_file, dst_file)
        return UploadResult(f"https://storage.cloud.google.com/{bucket}/{dst_file}")

    def generate_download_url(self, bucket, file, mins) -> str:
        try:
            return gcshus.generate_download_signed_url_with_token_refresh(
                self.gcs_client, bucket, file, mins * 60
            )
        except gcshus.NotServiceAccountException:
            raise NotServiceAccountException("GCS client is not a service account. ")


class S3(StorageService):
    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        boto3.resource("s3").Bucket(bucket).upload_file(src_file, dst_file)
        return UploadResult(f"https://{bucket}.s3.amazonaws.com/{dst_file}")

    def generate_download_url(self, bucket, file, mins) -> str:
        return boto3.client("s3").generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": file},
            ExpiresIn=mins * 60,
        )
