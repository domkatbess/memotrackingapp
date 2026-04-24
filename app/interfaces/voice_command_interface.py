"""Voice command parsing service abstraction interface.

Defines the contract for parsing text commands into structured intents.
Implementations include a mock adapter (Phase 1) and Amazon Lex (Phase 2).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class CommandIntent:
    """Result of parsing a voice command into a structured intent."""

    intent_name: str
    slots: dict[str, str] = field(default_factory=dict)
    confidence: float = 0.0


class VoiceCommandInterface(ABC):
    """Abstract base class for voice command parsing operations."""

    @abstractmethod
    async def parse_command(self, text: str, bot_id: str) -> CommandIntent:
        """Parse a text command into an intent with slots.

        Args:
            text: The text command to parse.
            bot_id: Identifier for the bot/model to use for parsing.

        Returns:
            A CommandIntent containing the identified intent name,
            extracted slots, and confidence score.
        """
        ...
