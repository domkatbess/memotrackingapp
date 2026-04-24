"""Mock notification adapter for development and testing.

Logs email sends instead of delivering them. Maintains a sent log
that can be inspected in tests.
"""

import logging
import uuid

from app.interfaces.notification_interface import (
    EmailMessage,
    NotificationInterface,
)

logger = logging.getLogger(__name__)


class MockNotificationAdapter(NotificationInterface):
    """Mock implementation of NotificationInterface.

    Instead of sending real emails, logs the message details and stores
    them in an in-memory list for test inspection.

    Attributes:
        sent_messages: List of all EmailMessage objects that were "sent".
    """

    def __init__(self) -> None:
        self.sent_messages: list[EmailMessage] = []

    async def send_email(self, message: EmailMessage) -> str:
        message_id = str(uuid.uuid4())
        self.sent_messages.append(message)
        logger.info(
            "MockNotification: email sent (id=%s, to=%s, subject=%s)",
            message_id,
            message.to,
            message.subject,
        )
        return message_id
