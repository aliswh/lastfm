from .abstract_ingestion_layer import DataLake
from google.cloud import storage
import json

class GoogleStorage(DataLake):

    def __init__(self, creds_path, bucket_name):

        self.client = storage.Client.from_service_account_json(creds_path)
        self.bucket = self.client.get_bucket(bucket_name)

    def write(self, data, dest_path, jsonize = False):
        blob = self.bucket.blob(dest_path)
        if jsonize:
            data = json.dumps(data)
        blob.upload_from_string(
            data = data,
            content_type='application/json'
        )
        return blob.public_url

    def read(self, file_path):
        blob = self.bucket.get_blob(file_path).download_as_string()
        file_data = json.loads(blob)
        return file_data

    def list_dir(self, path):
        return self.client.list_blobs(self.bucket, prefix=path)