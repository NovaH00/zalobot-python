"""Protocol interfaces defining the Zalo Bot API contract."""

from typing import Protocol
from ..types import MessageInfo

class ZaloBotAPI(Protocol):
    """Protocol defining the interface for Zalo Bot API operations.
    
    This protocol specifies the minimum required methods that a Zalo Bot
    implementation must provide. It's primarily used for type hints and
    dependency injection.
    """
    
    async def sendMessage(self, chat_id: str, text: str) -> MessageInfo:
        """Send a text message to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            text: The text content of the message.
        
        Returns:
            MessageInfo: Information about the sent message.
        """
        ...
    
    async def sendPhoto(self, chat_id: str, caption: str, photo_url: str) -> None:
        """Send a photo to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            caption: Caption text for the photo.
            photo_url: URL of the photo to send.
        """
        ...
    
    async def sendSticker(self, chat_id: str, sticker: str) -> None:
        """Send a sticker to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            sticker: The sticker identifier.
        """
        ...
    
    async def sendChatAction(self, chat_id: str, action: str) -> None:
        """Send a chat action to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            action: The action type (e.g., 'typing').
        """
        ...
