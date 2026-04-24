"""Local filesystem-based storage adapter.

Stores files on the local filesystem for development and testing.
Files are organized under a configurable base directory using bucket/key paths.
"""

import io
import os
from typing import BinaryIO

from app.interfaces.storage_interface import StorageInterface


class LocalStorageAdapter(StorageInterface):
    """Filesystem-based implementation of StorageInterface."""

    def __init__(self, base_dir: str = "local_storage") -> None:
        self.base_dir = base_dir

    def _resolve_path(self, bucket: str, key: str) -> str:
        """Build the full filesystem path for a bucket/key pair."""
        return os.path.join(self.base_dir, bucket, key)

    async def upload_file(
        self, bucket: str, key: str, file: BinaryIO, content_type: str
    ) -> str:
        path = self._resolve_path(bucket, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = file.read()
        with open(path, "wb") as f:
            f.write(data)
        return f"local://{bucket}/{key}"

    async def download_file(self, bucket: str, key: str) -> BinaryIO:
        path = self._resolve_path(bucket, key)
        with open(path, "rb") as f:
            data = f.read()
        return io.BytesIO(data)

    async def delete_file(self, bucket: str, key: str) -> None:
        path = self._resolve_path(bucket, key)
        if os.path.exists(path):
            os.remove(path)

    async def get_file_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        return f"local://{bucket}/{key}?expires_in={expires_in}"
