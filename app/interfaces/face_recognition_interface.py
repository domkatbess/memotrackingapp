"""Face recognition service abstraction interface.

Defines the contract for face detection, indexing, and comparison operations.
Implementations include a mock adapter (Phase 1) and Amazon Rekognition (Phase 2).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FaceMatch:
    """Result of a face comparison or search operation."""

    confidence: float
    face_id: str


class FaceRecognitionInterface(ABC):
    """Abstract base class for face recognition operations."""

    @abstractmethod
    async def detect_faces(self, image_bytes: bytes) -> list[dict]:
        """Detect faces in an image.

        Args:
            image_bytes: Raw image data.

        Returns:
            A list of dictionaries containing face details (bounding box,
            confidence, landmarks, etc.).
        """
        ...

    @abstractmethod
    async def index_face(
        self, collection_id: str, image_bytes: bytes, external_id: str
    ) -> str:
        """Index a face into a collection.

        Args:
            collection_id: The face collection to index into.
            image_bytes: Raw image data containing a face.
            external_id: An external identifier to associate with the face.

        Returns:
            The face_id assigned by the recognition service.
        """
        ...

    @abstractmethod
    async def compare_faces(
        self,
        source_image: bytes,
        target_image: bytes,
        threshold: float = 90.0,
    ) -> list[FaceMatch]:
        """Compare two face images.

        Args:
            source_image: Raw image data of the source face.
            target_image: Raw image data of the target face.
            threshold: Minimum confidence threshold for a match.

        Returns:
            A list of FaceMatch results above the threshold.
        """
        ...

    @abstractmethod
    async def search_faces_by_image(
        self,
        collection_id: str,
        image_bytes: bytes,
        threshold: float = 90.0,
    ) -> list[FaceMatch]:
        """Search a collection for matching faces.

        Args:
            collection_id: The face collection to search.
            image_bytes: Raw image data to search with.
            threshold: Minimum confidence threshold for a match.

        Returns:
            A list of FaceMatch results above the threshold.
        """
        ...

    @abstractmethod
    async def delete_faces(
        self, collection_id: str, face_ids: list[str]
    ) -> None:
        """Remove faces from a collection.

        Args:
            collection_id: The face collection to remove from.
            face_ids: List of face IDs to delete.
        """
        ...
