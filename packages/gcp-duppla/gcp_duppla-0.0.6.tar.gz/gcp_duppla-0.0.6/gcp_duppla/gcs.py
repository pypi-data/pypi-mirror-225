import os
import json
from google.cloud import storage
from typing import Iterator


class google_cloud_storage:
    def __init__(self, gcp_cred_location: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_cred_location
        with open(gcp_cred_location, "r") as f:
            project_id = json.load(f).get("project_id")
        self.client = storage.Client(project_id)

    # upload a file to a bucket
    def upload_blob(self, bucket: str, filename: str, gcs_filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(gcs_filename)
        blob.upload_from_filename(filename)

    # upload a file in memory to a bucket
    def upload_blob_from_memory(self, bucket: str, data: bytes, gcs_filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(gcs_filename)
        blob.upload_from_string(data)

    # download a file from a bucket
    def download_as_string(self, bucket: str, filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(filename)
        return blob.download_as_string(client=None)

    # list blobs in a bucket
    def list_blobs(self, bucket: str, prefix: str | None = None) -> Iterator:
        return self.client.list_blobs(bucket, prefix=prefix)
