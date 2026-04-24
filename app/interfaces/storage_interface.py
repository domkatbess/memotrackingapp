"""Storage service abstraction interface.

Defines the contract for file storage operations. Implementations include
local filesystem storage (Phase 1) and Amazon S3 (Phase 2).
"""

from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageInterface(ABC):
    """Abstract base class for file storage operations."""

    @abstractmethod
    async def upload_file(
        self, bucket: str, key: str, file: BinaryIO, content_type: str
    ) -> str:
        """Upload a file and return its storage URL.

        Args:
            bucket: Storage bucket/container name.
            key: Unique key identifying the file within the bucket.
            file: File-like object containing the data to upload.
            content_type: MIME type of the file.

        Returns:
            The storage URL or key of the uploaded file.
        """
        ...

    @abstractmethod
    async def download_file(self, bucket: str, key: str) -> BinaryIO:
        """Download a file by key.

        Args:
            bucket: Storage bucket/container name.
            key: Unique key identifying the file.

        Returns:
            A file-like object containing the file data.
        """
        ...

    @abstractmethod
    async def delete_file(self, bucket: str, key: str) -> None:
        """Delete a file by key.

        Args:
            bucket: Storage bucket/container name.
            key: Unique key identifying the file.
        """
        ...

    @abstractmethod
    async def get_file_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        """Generate a pre-signed URL for file access.

        Args:
            bucket: Storage bucket/container name.
            key: Unique key identifying the file.
            expires_in: URL expiration time in seconds (default 1 hour).

        Returns:
            A pre-signed URL string for accessing the file.
        """
        ...
