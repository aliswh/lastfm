from abstract_ingestion_layer import DataLake
from google.cloud import storage
import json

class GoogleStorage(DataLake):

    def __init__(self, creds_path, bucket_name):

        self.client = storage.Client.from_service_account_json(creds_path)
        self.bucket = self.client.get_bucket(bucket_name)

    def write(self, data, dest_path):
        blob = self.bucket.blob(dest_path)
        blob.upload_from_string(
            data = data,
            content_type='application/json'
        )
        return blob.public_url

    def read(self, file_path):
        blob = self.bucket.get_blob(file_path)
        file_data = json.load(blob)
        return file_data