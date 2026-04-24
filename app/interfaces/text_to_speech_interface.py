"""Text-to-speech service abstraction interface.

Defines the contract for converting text to speech audio.
Implementations include a mock adapter (Phase 1) and Amazon Polly (Phase 2).
"""

from abc import ABC, abstractmethod


class TextToSpeechInterface(ABC):
    """Abstract base class for text-to-speech operations."""

    @abstractmethod
    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "Aditi",
        output_format: str = "mp3",
    ) -> bytes:
        """Convert text to speech audio bytes.

        Args:
            text: The text to convert to speech.
            voice_id: The voice to use for synthesis (default "Aditi").
            output_format: Audio output format (default "mp3").

        Returns:
            Raw audio bytes in the specified format.
        """
        ...
