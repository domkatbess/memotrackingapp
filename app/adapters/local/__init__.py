"""Local/mock adapter implementations for all service abstraction interfaces.

These adapters provide deterministic, configurable responses for development
and testing (Phase 1). They are replaced by AWS adapters in Phase 2.
"""

from app.adapters.local.local_storage_adapter import LocalStorageAdapter
from app.adapters.local.mock_face_recognition_adapter import (
    MockFaceRecognitionAdapter,
)
from app.adapters.local.mock_notification_adapter import MockNotificationAdapter
from app.adapters.local.mock_text_to_speech_adapter import (
    MockTextToSpeechAdapter,
)
from app.adapters.local.mock_voice_command_adapter import (
    MockVoiceCommandAdapter,
)
from app.adapters.local.mock_voice_transcription_adapter import (
    MockVoiceTranscriptionAdapter,
)

__all__ = [
    "LocalStorageAdapter",
    "MockFaceRecognitionAdapter",
    "MockVoiceTranscriptionAdapter",
    "MockVoiceCommandAdapter",
    "MockTextToSpeechAdapter",
    "MockNotificationAdapter",
]
