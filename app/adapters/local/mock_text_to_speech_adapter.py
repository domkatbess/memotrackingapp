"""Mock text-to-speech adapter for development and testing.

Returns deterministic placeholder audio bytes.
"""

from app.interfaces.text_to_speech_interface import TextToSpeechInterface


class MockTextToSpeechAdapter(TextToSpeechInterface):
    """Mock implementation of TextToSpeechInterface.

    Returns a fixed byte sequence representing placeholder audio data.
    The content encodes the input text length so tests can verify
    the adapter was called with the expected input.
    """

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "Aditi",
        output_format: str = "mp3",
    ) -> bytes:
        # Return deterministic bytes that encode the input text for testability.
        header = f"MOCK_AUDIO|voice={voice_id}|format={output_format}|len={len(text)}|"
        return header.encode("utf-8") + text.encode("utf-8")
