import base64
import hashlib
import os
from io import BufferedReader

import requests

from dynamofl.datasets.dataset import Dataset
from dynamofl.models.model import Model

CHUNK_SIZE = 1024 * 1024  # 1MB


class LocalModel(Model):
    def __init__(
        self,
        request,
        name: str,
        key: str,
        model_file_path: str,
        dataset_file_path: str,
        config,
    ) -> None:
        self.request = request
        model_file_url = self.upload_model_file(
            key=key, model_file_path=model_file_path
        )
        config["url"] = model_file_url

        super().__init__(
            request=request,
            name=name,
            key=key,
            dataset_file_path=dataset_file_path,
            config=config,
            type="LOCAL",
        )

    def calculate_sha1_hash_base64(self, f: BufferedReader):
        # Read the file in chunks
        sha1 = hashlib.sha1()
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            sha1.update(data)
        # Seek back to the beginning of the file
        f.seek(0)
        return base64.b64encode(sha1.digest()).decode("utf-8")

    def upload_file(self, key: str, file_path: str, endpoint_url: str):
        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            sha1_hash = self.calculate_sha1_hash_base64(f)
            # Seek back to the beginning of the file
            f.seek(0)
            params = {
                "filename": file_name,
                "key": key,
                "sha1Checksum": sha1_hash,
            }
            res = self.request._make_request("POST", endpoint_url, params=params)
            presigned_url = res["url"]
            r = requests.put(
                presigned_url,
                data=f,
                headers={
                    # Specifying this header is important for AWS to verify the checksum.
                    # If you'll omit it, you'll receive a signature mismatch error.
                    # If you'll specify it incorrectly, you'll receive a checksum mismatch error.
                    "x-amz-checksum-sha1": sha1_hash,
                },
            )
            return res

    def upload_model_file(self, key: str, model_file_path: str):
        res = self.upload_file(key, model_file_path, "/ml-model/presigned-url")
        return res["objKey"]

    def upload_dataset_file(self, key: str, model_file_path: str):
        res = self.upload_file(key, model_file_path, "/dataset/presigned-url")
        return res["objKey"]

    def attach_dataset(self, dataset: Dataset):
        params = {"modelKey": self.key, "datasetId": dataset._id}
        res = self.request._make_request("PATCH", "/ml-model", params=params)
        print(res)
