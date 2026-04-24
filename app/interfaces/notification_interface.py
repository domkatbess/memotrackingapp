"""Notification service abstraction interface.

Defines the contract for sending email notifications.
Implementations include a mock/log-based adapter (Phase 1) and Amazon SES (Phase 2).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class EmailMessage:
    """Represents an email notification to be sent."""

    to: list[str] = field(default_factory=list)
    subject: str = ""
    body_html: str = ""
    body_text: str = ""


class NotificationInterface(ABC):
    """Abstract base class for notification delivery operations."""

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> str:
        """Send an email notification.

        Args:
            message: The EmailMessage to send.

        Returns:
            A message ID or identifier for the sent notification.
        """
        ...
