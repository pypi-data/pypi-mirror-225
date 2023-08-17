import unittest
import stowrap
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import os

load_dotenv()


class TestUpload(unittest.TestCase):
    def upload_test_file(self, service, bucket, filename) -> stowrap.UploadResult:
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return stowrap.Client(service).upload(bucket, testfile, filename)

    def test_gcs_upload(self):
        result = self.upload_test_file("gcs", os.environ["TEST_GCS_BUCKET"], "test.txt")
        self.assertTrue(result.url.startswith("https://storage.cloud.google.com/"))

    def test_s3_upload(self):
        bucket = os.environ["TEST_S3_BUCKET"]
        result = self.upload_test_file("s3", bucket, "test.txt")
        self.assertTrue(
            result.url.startswith(f"https://{bucket}.s3.amazonaws.com/"),
            f"url is {result.url}",
        )

    def test_gcs_generate_download_url(self):
        self.upload_test_file("gcs", os.environ["TEST_GCS_BUCKET"], "test.txt")
        try:
            url = stowrap.Client("gcs").generate_download_url(
                os.environ["TEST_GCS_BUCKET"], "test.txt", 5
            )
        except stowrap.NotServiceAccountException:
            self.skipTest("Not a service account")
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

    def test_s3_generate_download_url(self):
        bucket = os.environ["TEST_S3_BUCKET"]
        self.upload_test_file("s3", bucket, "test.txt")
        url = stowrap.Client("s3").generate_download_url(bucket, "test.txt", 5)
        self.assertTrue(
            url.startswith(f"https://{bucket}.s3.amazonaws.com/"),
            f"url is {url}",
        )


if __name__ == "__main__":
    unittest.main()
