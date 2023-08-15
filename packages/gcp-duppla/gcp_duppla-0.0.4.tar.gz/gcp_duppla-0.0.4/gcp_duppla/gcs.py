import os
import json
from google.cloud import storage


class google_cloud_storage:
    def __init__(self, gcp_cred_location: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_cred_location
        with open(gcp_cred_location, "r") as f:
            project_id = json.load(f).get("project_id")
        self.client = storage.Client(project_id)

    def upload_blob(self, bucket: str, filename: str, gcs_filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(gcs_filename)
        blob.upload_from_filename(filename)

    def upload_blob_from_memory(self, bucket: str, data: bytes, gcs_filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(gcs_filename)
        blob.upload_from_string(data)

    def download_as_string(self, bucket: str, filename: str):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(filename)
        return blob.download_as_string(client=None)

    def list_blobs(self, bucket: str, prefix: str):
        return self.client.list_blobs(bucket, prefix=prefix)
