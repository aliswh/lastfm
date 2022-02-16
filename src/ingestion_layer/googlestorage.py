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

    def read(self, path, dir=False):
        if dir:
            blobs = self.client.list_blobs(self.bucket, prefix=path)
            data = [json.loads(blob.download_as_string()) for blob in blobs]
        else:
            blob = self.bucket.get_blob(path).download_as_string()
            data = json.loads(blob)
        return data