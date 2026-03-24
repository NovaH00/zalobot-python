"""Entity models representing Zalo API data structures.

This module contains Pydantic models for various entities used in the Zalo Bot API,
including bot information, messages, events, and chat data.
"""

from enum import StrEnum
from pydantic import BaseModel, Field

from .responses import Result

class BotInfo(Result):
    """Bot information model containing details about the bot.
    
    Attributes:
        id: The unique identifier of the bot.
        account_name: The account name of the bot.
        account_type: The type of account (e.g., 'official', 'personal').
        can_join_groups: Whether the bot can join group chats.
        display_name: The display name shown to users.
    """
    id: str
    account_name: str
    account_type: str
    can_join_groups: bool
    display_name: str

class WebhookInfo(Result):
    """Webhook information model containing webhook configuration details.
    
    Attributes:
        url: The configured webhook URL.
        updated_at: Unix timestamp of when the webhook was last updated.
    """
    url: str
    updated_at: int

class MessageInfo(Result):
    """Message information model returned after sending a message.
    
    Attributes:
        message_id: The unique identifier of the sent message.
        date: Unix timestamp of when the message was sent.
    """
    message_id: str
    date: int

class EventName(StrEnum):
    """Enumeration of all possible event types from the Zalo API.
    
    Attributes:
        TEXT_RECEIVED: A text message was received.
        IMAGE_RECEIVED: An image message was received.
        STICKER_RECEIVED: A sticker message was received.
        UNSUPPORTED_RECEIVED: An unsupported message type was received.
    """
    TEXT_RECEIVED        = "message.text.received"
    IMAGE_RECEIVED       = "message.image.received"
    STICKER_RECEIVED     = "message.sticker.received"
    UNSUPPORTED_RECEIVED = "message.unsupported.received"

class From(BaseModel):
    """Sender information"""
    id: str
    display_name: str
    is_bot: bool

class Chat(BaseModel):
    """Current chat information"""
    id: str
    chat_type: str

class Message(BaseModel):
    """Message model representing an incoming message.
    
    Attributes:
        sender: The sender of the message.
        chat: The chat where the message was sent.
        text: The text content of the message.
        message_id: The unique identifier of the message.
        date: Unix timestamp of when the message was sent.
    """
    sender: From = Field(alias="from")
    chat: Chat
    text: str
    message_id: str
    date: int

class Event(Result):
    """Event model representing an incoming webhook event.
    
    Attributes:
        event_name: The type of event received.
        message: The message associated with the event.
    """
    event_name: EventName
    message: Message
