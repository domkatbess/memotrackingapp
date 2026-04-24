"""Mock face recognition adapter for development and testing.

Returns deterministic, configurable responses. By default, all operations
succeed with high confidence. Behavior can be customized per instance for
testing failure scenarios.
"""

import uuid

from app.interfaces.face_recognition_interface import (
    FaceMatch,
    FaceRecognitionInterface,
)


class MockFaceRecognitionAdapter(FaceRecognitionInterface):
    """Mock implementation of FaceRecognitionInterface.

    Attributes:
        detect_faces_result: Configurable result for detect_faces calls.
        match_confidence: Confidence score returned for compare/search operations.
        should_detect_face: Whether detect_faces returns a detected face.
        should_match: Whether compare/search operations return a match.
    """

    def __init__(
        self,
        match_confidence: float = 99.5,
        should_detect_face: bool = True,
        should_match: bool = True,
    ) -> None:
        self.match_confidence = match_confidence
        self.should_detect_face = should_detect_face
        self.should_match = should_match
        # Track indexed faces for testing
        self._indexed_faces: dict[str, list[str]] = {}

    async def detect_faces(self, image_bytes: bytes) -> list[dict]:
        if not self.should_detect_face:
            return []
        return [
            {
                "BoundingBox": {
                    "Width": 0.5,
                    "Height": 0.6,
                    "Left": 0.25,
                    "Top": 0.2,
                },
                "Confidence": self.match_confidence,
                "Landmarks": [],
            }
        ]

    async def index_face(
        self, collection_id: str, image_bytes: bytes, external_id: str
    ) -> str:
        face_id = str(uuid.uuid4())
        if collection_id not in self._indexed_faces:
            self._indexed_faces[collection_id] = []
        self._indexed_faces[collection_id].append(face_id)
        return face_id

    async def compare_faces(
        self,
        source_image: bytes,
        target_image: bytes,
        threshold: float = 90.0,
    ) -> list[FaceMatch]:
        if not self.should_match:
            return []
        return [
            FaceMatch(
                confidence=self.match_confidence,
                face_id=str(uuid.uuid4()),
            )
        ]

    async def search_faces_by_image(
        self,
        collection_id: str,
        image_bytes: bytes,
        threshold: float = 90.0,
    ) -> list[FaceMatch]:
        if not self.should_match:
            return []
        face_ids = self._indexed_faces.get(collection_id, [])
        if face_ids:
            return [
                FaceMatch(confidence=self.match_confidence, face_id=face_ids[0])
            ]
        return [
            FaceMatch(
                confidence=self.match_confidence,
                face_id=str(uuid.uuid4()),
            )
        ]

    async def delete_faces(
        self, collection_id: str, face_ids: list[str]
    ) -> None:
        if collection_id in self._indexed_faces:
            self._indexed_faces[collection_id] = [
                fid
                for fid in self._indexed_faces[collection_id]
                if fid not in face_ids
            ]
