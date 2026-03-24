"""Context module for webhook handler execution.

This module provides the Context class, which encapsulates the current event
and provides convenient methods for responding to messages.
"""

from typing import final
from ..types import Event, EventName, MessageInfo, From, Chat
from .interfaces import ZaloBotAPI

@final
class Context:
    """Context object passed to webhook handlers.
    
    The Context provides access to the incoming event data and convenient methods
    for responding to messages. It's the primary interface for webhook handlers
    to interact with incoming messages.
    
    Example:
        ```python
        async def my_handler(ctx: Context):
            if ctx.is_text:
                await ctx.reply(f"You said: {ctx.text}")
        ```
    """
    
    def __init__(self, *, _update: Event, _bot: ZaloBotAPI):
        """Initialize a new Context instance.
        
        Args:
            _update: The event object containing the incoming message data.
            _bot: The bot instance used for sending responses.
        """
        self._update = _update
        self._bot = _bot

    async def reply(self, text: str) -> MessageInfo:
        """Reply to the current message with text.
        
        This is a convenience method that sends a message to the same chat
        as the incoming message.
        
        Args:
            text: The text content of the reply message.
        
        Returns:
            MessageInfo: Information about the sent reply message.
        
        Example:
            ```python
            await ctx.reply("Hello!")
            ```
        """
        return await self._bot.sendMessage(self.chat_id, text)

    @property
    def chat_id(self) -> str:
        """Get the unique identifier of the current chat.
        
        Returns:
            str: The chat ID where the message was sent.
        """
        return self._update.message.chat.id

    @property
    def user_id(self) -> str:
        """Get the unique identifier of the message sender.
        
        Returns:
            str: The user ID of the person who sent the message.
        """
        return self._update.message.sender.id

    @property
    def text(self) -> str:
        """Get the text content of the message.
        
        Returns:
            str: The message text. Empty if the message is not text.
        """
        return self._update.message.text

    @property
    def message_id(self) -> str:
        """Get the unique identifier of the message.
        
        Returns:
            str: The message ID.
        """
        return self._update.message.message_id

    @property
    def sender(self) -> From:
        """Get information about the message sender.
        
        Returns:
            From: The sender's information including ID and display name.
        """
        return self._update.message.sender

    @property
    def chat(self) -> Chat:
        """Get information about the current chat.
        
        Returns:
            Chat: The chat information including ID and chat type.
        """
        return self._update.message.chat

    @property
    def is_text(self) -> bool:
        """Check if the message is a text message.
        
        Returns:
            bool: True if the event is a text message, False otherwise.
        """
        return self._update.event_name == EventName.TEXT_RECEIVED

    @property
    def is_image(self) -> bool:
        """Check if the message is an image.
        
        Returns:
            bool: True if the event is an image message, False otherwise.
        """
        return self._update.event_name == EventName.IMAGE_RECEIVED

    @property
    def is_sticker(self) -> bool:
        """Check if the message is a sticker.
        
        Returns:
            bool: True if the event is a sticker message, False otherwise.
        """
        return self._update.event_name == EventName.STICKER_RECEIVED

    @property
    def is_unsupported(self) -> bool:
        """Check if the message type is unsupported.
        
        Returns:
            bool: True if the event type is unsupported, False otherwise.
        """
        return self._update.event_name == EventName.UNSUPPORTED_RECEIVED
