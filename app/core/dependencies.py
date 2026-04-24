"""Dependency injection setup for service abstraction interfaces.

Wires abstract interfaces to concrete adapter implementations.
In Phase 1, all interfaces are bound to local/mock adapters.
In Phase 2, AWS adapters can be selected via configuration.
"""

from functools import lru_cache

from app.adapters.local import (
    LocalStorageAdapter,
    MockFaceRecognitionAdapter,
    MockNotificationAdapter,
    MockTextToSpeechAdapter,
    MockVoiceCommandAdapter,
    MockVoiceTranscriptionAdapter,
)
from app.interfaces import (
    FaceRecognitionInterface,
    NotificationInterface,
    StorageInterface,
    TextToSpeechInterface,
    VoiceCommandInterface,
    VoiceTranscriptionInterface,
)


@lru_cache
def get_storage_service() -> StorageInterface:
    """Provide a StorageInterface implementation.

    Returns LocalStorageAdapter in Phase 1.
    """
    return LocalStorageAdapter()


@lru_cache
def get_face_recognition_service() -> FaceRecognitionInterface:
    """Provide a FaceRecognitionInterface implementation.

    Returns MockFaceRecognitionAdapter in Phase 1.
    """
    return MockFaceRecognitionAdapter()


@lru_cache
def get_voice_transcription_service() -> VoiceTranscriptionInterface:
    """Provide a VoiceTranscriptionInterface implementation.

    Returns MockVoiceTranscriptionAdapter in Phase 1.
    """
    return MockVoiceTranscriptionAdapter()


@lru_cache
def get_voice_command_service() -> VoiceCommandInterface:
    """Provide a VoiceCommandInterface implementation.

    Returns MockVoiceCommandAdapter in Phase 1.
    """
    return MockVoiceCommandAdapter()


@lru_cache
def get_text_to_speech_service() -> TextToSpeechInterface:
    """Provide a TextToSpeechInterface implementation.

    Returns MockTextToSpeechAdapter in Phase 1.
    """
    return MockTextToSpeechAdapter()


@lru_cache
def get_notification_service() -> NotificationInterface:
    """Provide a NotificationInterface implementation.

    Returns MockNotificationAdapter in Phase 1.
    """
    return MockNotificationAdapter()
