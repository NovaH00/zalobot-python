from enum import StrEnum 
from pydantic import BaseModel, Field

from .responses import Result

class BotInfo(Result):
    id: str  
    account_name: str 
    account_type: str 
    can_join_groups: bool
    display_name: str

class WebhookInfo(Result):
    url: str 
    updated_at: int 

class MessageInfo(Result):
    message_id: str
    date: int

class EventName(StrEnum):
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
    sender: From = Field(alias="from")
    chat: Chat
    text: str
    message_id: str
    date: int

class Event(Result):
    event_name: EventName
    message: Message
