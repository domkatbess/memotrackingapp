"""Mock voice transcription adapter for development and testing.

Returns deterministic, configurable transcription results.
"""

from app.interfaces.voice_transcription_interface import (
    TranscriptionResult,
    VoiceTranscriptionInterface,
)


class MockVoiceTranscriptionAdapter(VoiceTranscriptionInterface):
    """Mock implementation of VoiceTranscriptionInterface.

    Attributes:
        default_text: The text returned by transcription calls.
        default_confidence: The confidence score returned.
    """

    def __init__(
        self,
        default_text: str = "This is a mock transcription of the audio content.",
        default_confidence: float = 0.95,
    ) -> None:
        self.default_text = default_text
        self.default_confidence = default_confidence

    async def transcribe_audio(
        self, audio_bytes: bytes, language_code: str = "en-US"
    ) -> TranscriptionResult:
        return TranscriptionResult(
            text=self.default_text,
            confidence=self.default_confidence,
            language_code=language_code,
        )
