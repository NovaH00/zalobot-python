"""
Core module implementing the main ZaloBot class and webhook management.

This module contains the primary bot implementation with support for both
polling (getUpdates) and webhook-based event handling.
"""

import secrets
from typing import Annotated, Protocol

from ..types import (
    ErrorResponse,
    ZaloAPIError,
    BotInfo,
    WebhookInfo,
    MessageInfo,
    Event
)
from ..config import ZaloAPIConfig
from .http import fetch
from .context import Context

class UnconfiguredWebhook:
    """Represents the state of the bot where webhook have not yet configured"""
class ConfiguredWebhook:
    """Represents the state of the bot where webhook is configured"""
type BotStates = Annotated[
    UnconfiguredWebhook | ConfiguredWebhook,
    "Represents the states of the bot"
]

class AsyncWebhookHandler(Protocol):
    """Protocol for asynchronous webhook handlers.
    
    Handlers are callable objects that accept a Context and process incoming webhook events.
    """
    async def __call__(self, ctx: Context) -> None: ...

class ZaloBot[S: BotStates = UnconfiguredWebhook]:
    """Main ZaloBot class for interacting with the Zalo Bot API.
    
    This class provides a type-safe interface for all Zalo Bot API operations,
    supporting both polling and webhook-based event handling.
    
    Type Parameters:
        S: The bot state (UnconfiguredWebhook or ConfiguredWebhook)
    
    Example:
        Basic usage with polling:
        ```python
        bot = ZaloBot("your_bot_token")
        info = await bot.getMe()
        ```
        
        Webhook setup:
        ```python
        bot = ZaloBot("your_bot_token")
        configured_bot = await bot.configure_webhook("https://your-domain.com/webhook")
        configured_bot.add_webhook_handler(my_handler)
        ```
    """
    
    def __init__(
        self,
        BOT_TOKEN: str,
        *,
        _secret_token: str | None = None
    ):
        """Initialize a new ZaloBot instance.
        
        Args:
            BOT_TOKEN: The bot token obtained from Zalo Bot Platform.
            _secret_token: Optional secret token for webhook verification.
                          Typically set automatically when configuring webhooks.
        """
        self._BOT_TOKEN: str = BOT_TOKEN
        self._base_url: str = f"{ZaloAPIConfig.BASE_URL}/bot{BOT_TOKEN}"
        self._webhook_handlers: list[AsyncWebhookHandler] = []
        if _secret_token is not None:
            self._secret_token: str = _secret_token

    async def getMe(self) -> BotInfo:
        """Get information about the bot.
        
        Returns:
            BotInfo: The bot's information including ID, name, and capabilities.
        
        Raises:
            ZaloAPIError: If the API request fails.
        
        Example:
            ```python
            bot_info = await bot.getMe()
            print(f"Bot name: {bot_info.display_name}")
            ```
        """
        url = f"{self._base_url}/getMe"

        res = await fetch(url, result_schema=BotInfo)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def getUpdates(self, timeout: int = 30) -> Event:
        """Poll for new updates from the Zalo API.
        
        This method uses long polling to wait for new events. It's an alternative
        to using webhooks for receiving messages.
        
        Args:
            timeout: Maximum time in seconds to wait for new updates. Defaults to 30.
        
        Returns:
            Event: The latest event received.
        
        Raises:
            ZaloAPIError: If the API request fails.
        
        Example:
            ```python
            while True:
                event = await bot.getUpdates(timeout=30)
                # Process event
            ```
        """
        url = f"{self._base_url}/getUpdates"

        payload = {
            "timeout": timeout
        }

        res = await fetch(url, result_schema=Event, method="POST", body=payload, timeout=timeout)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def setWebhook(
        self: ZaloBot[UnconfiguredWebhook],
        webhook_url: str,
        secret_token: str,
    ) -> WebhookInfo:
        """Set a webhook for receiving updates.
        
        Registers a URL where Zalo will send POST requests for new events.
        
        Args:
            webhook_url: The HTTPS URL to receive webhook updates.
            secret_token: Secret token for verifying webhook authenticity.
        
        Returns:
            WebhookInfo: Information about the configured webhook.
        
        Raises:
            ZaloAPIError: If the API request fails.
        
        Note:
            This method can only be called on bots in UnconfiguredWebhook state.
        """
        url = f"{self._base_url}/setWebhook"

        payload = {
            "url": webhook_url,
            "secret_token": secret_token
        }

        res = await fetch(url, result_schema=WebhookInfo, method="POST", body=payload)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def deleteWebhook(self) -> WebhookInfo:
        """Delete the current webhook configuration.

        This method deletes the webhook if one exists.

        Note:
            Unlike some APIs, this method succeeds even if no webhook is currently
            configured. This allows you to safely call it at any time to ensure
            a clean state before reconfiguring.

            The API returns a WebhookInfo with empty/default values (empty URL and
            current timestamp) rather than information about the deleted webhook.

        Returns:
            WebhookInfo: Webhook info with empty URL and current timestamp.

        Example:
            ```python
            # Safely delete webhook (even if none exists)
            await bot.deleteWebhook()
            ```
        """
        url = f"{self._base_url}/deleteWebhook"

        res = await fetch(url, result_schema=WebhookInfo)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result 

    async def getWebhookInfo(self) -> WebhookInfo:
        """Get information about the current webhook configuration.
        
        Returns:
            WebhookInfo: Current webhook URL and status.
        
        Raises:
            ZaloAPIError: If the API request fails or no webhook exists.
        """
        url = f"{self._base_url}/getWebhookInfo"

        res = await fetch(url, result_schema=WebhookInfo)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def sendMessage(self, chat_id: str, text: str) -> MessageInfo:
        """Send a text message to a chat.
        
        Args:
            chat_id: The unique identifier of the chat to send the message to.
            text: The text content of the message.
        
        Returns:
            MessageInfo: Information about the sent message including message ID and date.
        
        Raises:
            ZaloAPIError: If the API request fails.
        
        Example:
            ```python
            result = await bot.sendMessage("chat_123", "Hello, World!")
            print(f"Message sent with ID: {result.message_id}")
            ```
        """
        url = f"{self._base_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }
        res = await fetch(url, result_schema=MessageInfo, method="POST", body=payload)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result


    async def sendPhoto(self, chat_id: str, caption: str, photo_url: str) -> None:
        """Send a photo to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            caption: Caption text for the photo.
            photo_url: URL of the photo to send.
        
        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError()

    async def sendSticker(self, chat_id: str, sticker: str) -> None:
        """Send a sticker to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            sticker: The sticker identifier.
        
        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError()

    async def sendChatAction(self, chat_id: str, action: str) -> None:
        """Send a chat action (e.g., typing, uploading) to a chat.
        
        Args:
            chat_id: The unique identifier of the chat.
            action: The action type (e.g., 'typing', 'upload_photo').
        
        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError()

    async def configure_webhook(
        self: ZaloBot[UnconfiguredWebhook],
        url: str
    ) -> ZaloBot[ConfiguredWebhook]:
        """Upgrades the bot to support webhook mechanisms.

        This method sets up the webhook with Zalo API and generates a secret token
        for secure webhook verification. Returns a new ZaloBot instance in the
        ConfiguredWebhook state.

        Note:
            This method first calls `deleteWebhook()` to ensure a clean state before
            setting the new webhook. This prevents errors if a webhook was previously
            configured.

        Args:
            url: The HTTPS URL to receive webhook updates.

        Returns:
            ZaloBot[ConfiguredWebhook]: A new bot instance with webhook configured.

        Warning:
            This method will raise a `ZaloAPIError` if the Zalo API fails to set
            the webhook.

        Example:
            ```python
            bot = ZaloBot("token")
            configured_bot = await bot.configure_webhook("https://example.com/webhook")
            ```
        """
        secret_token = secrets.token_urlsafe(192)
        _ = await self.deleteWebhook() 
        _ = await self.setWebhook(url, secret_token)

        return ZaloBot(self._BOT_TOKEN, _secret_token = secret_token)

    def get_secret_token(self: ZaloBot[ConfiguredWebhook]):
        """Gets the secret token generated by the configure_webhook.
        
        Returns:
            str: The secret token used for webhook verification.
        
        Note:
            The secret token is used to verify that webhook requests come from Zalo.
        """
        return self._secret_token

    def add_webhook_handler(
        self: ZaloBot[ConfiguredWebhook],
        handler: AsyncWebhookHandler
    ) -> None:
        """Registers a handler to handle on webhook event update.
        
        Args:
            handler: An async callable that accepts a Context object.
        
        Example:
            ```python
            async def my_handler(ctx: Context):
                if ctx.is_text:
                    await ctx.reply("Hello!")
            
            bot.add_webhook_handler(my_handler)
            ```
        """
        self._webhook_handlers.append(handler)

    async def dispatch_webhook_handlers(
        self: ZaloBot[ConfiguredWebhook],
        update_event: Event
    ) -> None:
        """Run all handlers given a webhook event.
        
        This method is called internally when a webhook event is received.
        It creates a Context for the event and passes it to all registered handlers.

        Args:
            update_event: The event object received from the webhook.
        """
        for handler in self._webhook_handlers:
            await handler(Context(_update=update_event, _bot=self))
