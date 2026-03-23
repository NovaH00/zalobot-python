from enum import StrEnum 
from typing import Literal, TypeVar, override, Annotated
from pydantic import BaseModel, Field

class Result(BaseModel):
    """Represents the result field in the Zalo API successful response"""
    pass

T = TypeVar("T", bound=Result)
class SuccessfulResponse[T](BaseModel):
    """Represents the successful response of the Zalo API"""
    ok: Literal[True] = True
    result: T = Field(description="The result when the API call is successful.")

class ErrorResponse(BaseModel):
    """Represents the error response of Zalo API"""
    ok: Literal[False] = False
    description: str = Field(description="The description of the error")
    error_code: int = Field(description="The error code")

type ZaloAPIResponse[T] = Annotated[
    SuccessfulResponse[T] | ErrorResponse,
    "Represents the response of the Zalo API"
]

class ZaloAPIError(BaseException):
    """Exception when using the Zalo API"""
    def __init__(self, error_code: int, description: str):
        self.error_code: int = error_code
        self.description: str = description
        super().__init__()

    @override
    def __str__(self):
        return f"error_code: {self.error_code}; description: {self.description}"

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

class Event(BaseModel):
    event_name: EventName
    message: Message
