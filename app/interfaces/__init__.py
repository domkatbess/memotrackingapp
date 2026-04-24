"""Service abstraction interfaces.

All external dependencies are accessed through abstract base classes defined here.
This enables swapping between local/mock implementations (Phase 1) and
AWS implementations (Phase 2) via dependency injection.
"""

from app.interfaces.face_recognition_interface import (
    FaceMatch,
    FaceRecognitionInterface,
)
from app.interfaces.notification_interface import (
    EmailMessage,
    NotificationInterface,
)
from app.interfaces.storage_interface import StorageInterface
from app.interfaces.text_to_speech_interface import TextToSpeechInterface
from app.interfaces.voice_command_interface import (
    CommandIntent,
    VoiceCommandInterface,
)
from app.interfaces.voice_transcription_interface import (
    TranscriptionResult,
    VoiceTranscriptionInterface,
)

__all__ = [
    # Storage
    "StorageInterface",
    # Face recognition
    "FaceRecognitionInterface",
    "FaceMatch",
    # Voice transcription
    "VoiceTranscriptionInterface",
    "TranscriptionResult",
    # Voice command
    "VoiceCommandInterface",
    "CommandIntent",
    # Text-to-speech
    "TextToSpeechInterface",
    # Notification
    "NotificationInterface",
    "EmailMessage",
]
