"""Voice transcription service abstraction interface.

Defines the contract for speech-to-text transcription operations.
Implementations include a mock adapter (Phase 1) and Amazon Transcribe (Phase 2).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TranscriptionResult:
    """Result of a voice transcription operation."""

    text: str
    confidence: float
    language_code: str


class VoiceTranscriptionInterface(ABC):
    """Abstract base class for voice transcription operations."""

    @abstractmethod
    async def transcribe_audio(
        self, audio_bytes: bytes, language_code: str = "en-US"
    ) -> TranscriptionResult:
        """Transcribe audio to text.

        Args:
            audio_bytes: Raw audio data.
            language_code: BCP-47 language code (default "en-US").

        Returns:
            A TranscriptionResult containing the transcribed text,
            confidence score, and language code.
        """
        ...
