"""
Types module containing all Pydantic models and type definitions for the Zalo API.

This module provides type-safe models for API requests, responses, and entities.
"""

from .responses import (
    ZaloAPIResponse,
    SuccessfulResponse,
    ErrorResponse,
    Result
)
from .entities import (
    BotInfo,
    MessageInfo,
    WebhookInfo,
    EventName,
    From,
    Chat,
    Message,
    Event
)
from .errors import ZaloAPIError

__all__ = [
    "SuccessfulResponse",
    "ErrorResponse",
    "ZaloAPIResponse",
    "Result",
    "BotInfo",
    "WebhookInfo",
    "MessageInfo",
    "EventName",
    "From",
    "Chat",
    "Message",
    "Event",
    "ZaloAPIError"
]
