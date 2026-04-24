"""Mock voice command parsing adapter for development and testing.

Returns deterministic, configurable command intents.
"""

from app.interfaces.voice_command_interface import (
    CommandIntent,
    VoiceCommandInterface,
)


class MockVoiceCommandAdapter(VoiceCommandInterface):
    """Mock implementation of VoiceCommandInterface.

    Attributes:
        default_intent: The intent name returned by parse_command.
        default_slots: The slots returned by parse_command.
        default_confidence: The confidence score returned.
    """

    def __init__(
        self,
        default_intent: str = "RetrieveMemo",
        default_slots: dict[str, str] | None = None,
        default_confidence: float = 0.92,
    ) -> None:
        self.default_intent = default_intent
        self.default_slots = default_slots or {"tracking_number": "MEMO-001"}
        self.default_confidence = default_confidence

    async def parse_command(self, text: str, bot_id: str) -> CommandIntent:
        return CommandIntent(
            intent_name=self.default_intent,
            slots=dict(self.default_slots),
            confidence=self.default_confidence,
        )
