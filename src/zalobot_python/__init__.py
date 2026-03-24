"""
ZaloBot Python SDK - A modern, fully-typed asynchronous SDK for Zalo Bot API.

This package provides an ergonomic and developer-friendly interface for building
Zalo chatbots with complete type safety and async support.
"""

from .zalobot import (
    ZaloBot,
    BotStates,
    UnconfiguredWebhook,
    ConfiguredWebhook,
    Context,
    AsyncWebhookHandler
)
from .types import (
    SuccessfulResponse,
    ErrorResponse,
    ZaloAPIResponse,
    BotInfo,
    WebhookInfo,
    MessageInfo,
    EventName,
    From,
    Chat,
    Message,
    Event,
    ZaloAPIError,
)

__all__ = [
    "SuccessfulResponse",
    "ErrorResponse",
    "ZaloAPIResponse",
    "ZaloBot",
    "Context",
    "AsyncWebhookHandler",
    "BotInfo",
    "WebhookInfo",
    "MessageInfo",
    "EventName",
    "From",
    "Chat",
    "Message",
    "Event",
    "ZaloAPIError",
    "BotStates",
    "UnconfiguredWebhook",
    "ConfiguredWebhook"
]
