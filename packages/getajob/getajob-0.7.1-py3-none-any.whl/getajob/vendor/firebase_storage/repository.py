from google.cloud.storage import Bucket

from .client_factory import FirebaseStorageClientFactory


class FirebaseStorageRepository:
    def __init__(self, client: Bucket = FirebaseStorageClientFactory.get_client()):
        self._client = client

    def upload_bytes(
        self,
        file_bytes: bytes,
        content_type: str,
        remote_file_path: str,
        publicly_accessible: bool = False,
    ) -> str:
        blob = self._client.blob(remote_file_path)
        blob.upload_from_string(data=file_bytes, content_type=content_type)
        if publicly_accessible:
            blob.make_public()
        return blob.public_url

    # def upload_file(self, local_file_path, remote_file_path, publicly_accessible: bool = False) -> str:
    #     blob = self._client.blob(remote_file_path)
    #     blob.upload_from_filename(local_file_path)
    #     if publicly_accessible:
    #         blob.make_public()
    #     return blob.public_url

    def update_file_public_access(
        self, remote_file_path, publicly_accessible: bool = False
    ) -> str:
        blob = self._client.blob(remote_file_path)
        if publicly_accessible:
            blob.make_public()
        else:
            blob.make_private()
        return blob.public_url

    # def download_to_file(self, remote_file_path, local_file_path) -> None:
    #     blob = self._client.blob(remote_file_path)
    #     blob.download_to_filename(local_file_path)

    def get_file_bytes(self, remote_file_path) -> bytes:
        blob = self._client.blob(remote_file_path)
        return blob.download_as_bytes()

    def delete_file(self, remote_file_path) -> None:
        blob = self._client.blob(remote_file_path)
        blob.delete()
