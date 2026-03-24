# ZaloBot Python SDK Documentation

A modern, fully-typed, asynchronous Python SDK for the Zalo Bot API.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
  - [Bot States](#bot-states)
  - [Webhook vs Polling](#webhook-vs-polling)
- [API Reference](#api-reference)
  - [ZaloBot](#zalobot)
  - [Context](#context)
  - [Types](#types)
  - [Errors](#errors)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)

---

## Overview

ZaloBot Python is a community-built SDK that provides an ergonomic and type-safe interface for building Zalo chatbots. It features:

- **Fully Typed**: Complete type hints for better IDE support and catch errors early
- **Asynchronous**: Built on `asyncio` and `httpx` for non-blocking I/O
- **Type-Safe States**: Generic types prevent invalid state transitions at compile time
- **Pydantic Models**: All API data is validated using Pydantic
- **Ergonomic Design**: Clean, intuitive API inspired by modern bot frameworks

---

## Installation

Install using `uv`:

```bash
uv add zalobot-python
```

Or using `pip`:

```bash
pip install zalobot-python
```

### Requirements

- Python 3.12+
- `httpx` for HTTP requests
- `pydantic` for data validation

---

## Quick Start

### 1. Create a Bot Instance

```python
from zalobot_python import ZaloBot

bot = ZaloBot("your_bot_token_here")
```

### 2. Get Bot Information

```python
bot_info = await bot.getMe()
print(f"Bot name: {bot_info.display_name}")
```

### 3. Set Up Webhook (Recommended for Production)

```python
from zalobot_python import Context

async def echo_handler(ctx: Context):
    """Echo back any text message"""
    if ctx.is_text:
        await ctx.reply(f"You said: {ctx.text}")

# Configure webhook
configured_bot = await bot.configure_webhook("https://your-domain.com/webhook")

# Register handler
configured_bot.add_webhook_handler(echo_handler)

# In your web server, when receiving a webhook event:
# await configured_bot.dispatch_webhook_handlers(event)
```

### 4. Use Polling (For Development)

```python
while True:
    event = await bot.getUpdates(timeout=30)
    if event.event_name == "message.text.received":
        await bot.sendMessage(
            event.message.chat.id,
            f"Echo: {event.message.text}"
        )
```

---

## Core Concepts

### Bot States

The SDK uses a type-state pattern to prevent invalid operations:

- **`UnconfiguredWebhook`**: Initial state. Bot can use polling or configure webhook.
- **`ConfiguredWebhook`**: After webhook is configured. Bot can handle webhook events.

```python
bot = ZaloBot("token")  # Type: ZaloBot[UnconfiguredWebhook]

# This is valid - transitioning from UnconfiguredWebhook to ConfiguredWebhook
configured_bot = await bot.configure_webhook("https://example.com")  # Type: ZaloBot[ConfiguredWebhook]

# This would be a type error - setWebhook only works on UnconfiguredWebhook
# await configured_bot.setWebhook(...)  # Type checker will catch this!
```

### Webhook vs Polling

| Feature | Webhook | Polling |
|---------|---------|---------|
| **Performance** | Real-time, push-based | Delayed, pull-based |
| **Resource Usage** | Low (only on events) | High (constant polling) |
| **Setup Complexity** | Requires HTTPS server | Simple, no server needed |
| **Best For** | Production | Development/Testing |

---

## API Reference

### ZaloBot

The main class for interacting with the Zalo Bot API.

#### Constructor

```python
ZaloBot(BOT_TOKEN: str, *, _secret_token: str | None = None)
```

- `BOT_TOKEN`: Your bot token from Zalo Bot Platform
- `_secret_token`: Internal use, set automatically by `configure_webhook()`

#### Methods

##### `getMe() -> BotInfo`

Get information about the bot.

**Returns:** Bot information including ID, name, and capabilities

**Example:**
```python
info = await bot.getMe()
print(f"Bot: {info.display_name}, Can join groups: {info.can_join_groups}")
```

##### `getUpdates(timeout: int = 30) -> Event`

Poll for new updates using long polling.

**Parameters:**
- `timeout`: Maximum seconds to wait for updates (default: 30)

**Returns:** The latest event

**Example:**
```python
event = await bot.getUpdates(timeout=30)
print(f"Event type: {event.event_name}")
```

##### `setWebhook(webhook_url: str, secret_token: str) -> WebhookInfo`

Set a webhook URL for receiving updates.

**Parameters:**
- `webhook_url`: HTTPS URL to receive webhook events
- `secret_token`: Secret token for verifying webhook authenticity

**Returns:** Webhook configuration info

**Note:** Only available on `ZaloBot[UnconfiguredWebhook]`

##### `deleteWebhook() -> WebhookInfo`

Delete the current webhook configuration.

**Returns:** WebhookInfo with empty URL and current timestamp

**Note:** Unlike some APIs, this method succeeds even if no webhook is currently
configured. The API returns a WebhookInfo with empty/default values rather than
information about the deleted webhook.

**Example:**
```python
# Safely delete webhook (even if none exists)
await bot.deleteWebhook()
```

##### `getWebhookInfo() -> WebhookInfo`

Get current webhook configuration.

**Returns:** Webhook URL and status

##### `sendMessage(chat_id: str, text: str) -> MessageInfo`

Send a text message to a chat.

**Parameters:**
- `chat_id`: Unique identifier of the chat
- `text`: Message text content

**Returns:** Info about the sent message

**Example:**
```python
result = await bot.sendMessage("chat_123", "Hello!")
print(f"Message ID: {result.message_id}")
```

##### `sendPhoto(chat_id: str, caption: str, photo_url: str) -> None`

Send a photo to a chat.

**Status:** Not yet implemented

##### `sendSticker(chat_id: str, sticker: str) -> None`

Send a sticker to a chat.

**Status:** Not yet implemented

##### `sendChatAction(chat_id: str, action: str) -> None`

Send a chat action (e.g., typing).

**Status:** Not yet implemented

##### `configure_webhook(url: str) -> ZaloBot[ConfiguredWebhook]`

Configure webhook and return a new bot instance in configured state.

**Parameters:**
- `url`: HTTPS URL for webhook events

**Returns:** New `ZaloBot` instance in `ConfiguredWebhook` state

**Note:** This method first calls `deleteWebhook()` to ensure a clean state before
setting the new webhook. This prevents errors if a webhook was previously configured.

**Warning:** Raises `ZaloAPIError` if the Zalo API fails to set the webhook.

**Example:**
```python
configured_bot = await bot.configure_webhook("https://example.com/webhook")
```

##### `get_secret_token() -> str`

Get the secret token for webhook verification.

**Returns:** The secret token string

**Note:** Only available on `ZaloBot[ConfiguredWebhook]`

##### `add_webhook_handler(handler: AsyncWebhookHandler) -> None`

Register a handler function for webhook events.

**Parameters:**
- `handler`: Async function that accepts a `Context` object

**Example:**
```python
async def handler(ctx: Context):
    await ctx.reply("Hello!")

bot.add_webhook_handler(handler)
```

##### `dispatch_webhook_handlers(update_event: Event) -> None`

Dispatch an event to all registered handlers.

**Parameters:**
- `update_event`: The event received from webhook

**Note:** Called internally by your web server

---

### Context

Context object passed to webhook handlers, providing access to event data and reply methods.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `chat_id` | `str` | ID of the current chat |
| `user_id` | `str` | ID of the message sender |
| `text` | `str` | Text content of the message |
| `message_id` | `str` | Unique message identifier |
| `sender` | `From` | Sender information object |
| `chat` | `Chat` | Chat information object |
| `is_text` | `bool` | True if message is text |
| `is_image` | `bool` | True if message is image |
| `is_sticker` | `bool` | True if message is sticker |
| `is_unsupported` | `bool` | True if message type unsupported |

#### Methods

##### `reply(text: str) -> MessageInfo`

Reply to the current message.

**Parameters:**
- `text`: Reply message text

**Returns:** Info about the sent reply

**Example:**
```python
async def handler(ctx: Context):
    await ctx.reply("Thanks for your message!")
```

---

### Types

#### BotInfo

Bot information model.

**Fields:**
- `id`: Bot's unique identifier
- `account_name`: Account name
- `account_type`: Account type (e.g., "official")
- `can_join_groups`: Whether bot can join groups
- `display_name`: Display name shown to users

#### WebhookInfo

Webhook configuration info.

**Fields:**
- `url`: Configured webhook URL
- `updated_at`: Unix timestamp of last update

#### MessageInfo

Message sending result.

**Fields:**
- `message_id`: Sent message ID
- `date`: Unix timestamp of sending

#### Event

Incoming webhook event.

**Fields:**
- `event_name`: Type of event (`EventName` enum)
- `message`: Message object

#### EventName

Enumeration of event types:

- `TEXT_RECEIVED` - "message.text.received"
- `IMAGE_RECEIVED` - "message.image.received"
- `STICKER_RECEIVED` - "message.sticker.received"
- `UNSUPPORTED_RECEIVED` - "message.unsupported.received"

#### From

Sender information.

**Fields:**
- `id`: User ID
- `display_name`: User's display name
- `is_bot`: Whether sender is a bot

#### Chat

Chat information.

**Fields:**
- `id`: Chat ID
- `chat_type`: Type of chat (e.g., "private", "group")

#### Message

Message object.

**Fields:**
- `sender`: Sender info (`From`)
- `chat`: Chat info (`Chat`)
- `text`: Message text
- `message_id`: Message ID
- `date`: Unix timestamp

---

### Errors

#### ZaloAPIError

Exception raised when the Zalo API returns an error.

**Attributes:**
- `error_code`: Numeric error code
- `description`: Human-readable error description

**Example:**
```python
try:
    await bot.sendMessage("invalid", "Hello")
except ZaloAPIError as e:
    print(f"Error {e.error_code}: {e.description}")
```

---

## Examples

### Echo Bot (Webhook)

```python
from zalobot_python import ZaloBot, Context

async def echo_handler(ctx: Context):
    if ctx.is_text:
        await ctx.reply(f"Echo: {ctx.text}")

bot = ZaloBot("your_token")
configured_bot = await bot.configure_webhook("https://your-domain.com/webhook")
configured_bot.add_webhook_handler(echo_handler)

# In your web server (e.g., FastAPI):
# @app.post("/webhook")
# async def webhook(request: Request):
#     event = Event.model_validate(await request.json())
#     await configured_bot.dispatch_webhook_handlers(event)
```

### Echo Bot (Polling)

```python
from zalobot_python import ZaloBot, EventName

bot = ZaloBot("your_token")

while True:
    event = await bot.getUpdates(timeout=30)
    
    if event.event_name == EventName.TEXT_RECEIVED:
        await bot.sendMessage(
            event.message.chat.id,
            f"Echo: {event.message.text}"
        )
```

### Command Handler

```python
from zalobot_python import Context

async def command_handler(ctx: Context):
    if ctx.is_text:
        text = ctx.text.lower()
        
        if text == "/start":
            await ctx.reply("Welcome! Send me a message.")
        elif text == "/help":
            await ctx.reply("I can echo your messages!")
        elif text.startswith("/echo "):
            await ctx.reply(text[6:])  # Remove "/echo " prefix

bot = ZaloBot("token")
configured_bot = await bot.configure_webhook("https://example.com/webhook")
configured_bot.add_webhook_handler(command_handler)
```

### Multi-Handler Setup

```python
from zalobot_python import Context

async def log_handler(ctx: Context):
    print(f"Message from {ctx.sender.display_name}: {ctx.text}")

async def response_handler(ctx: Context):
    if ctx.is_text:
        await ctx.reply("I received your message!")

bot = ZaloBot("token")
configured_bot = await bot.configure_webhook("https://example.com/webhook")
configured_bot.add_webhook_handler(log_handler)
configured_bot.add_webhook_handler(response_handler)
# Both handlers will be called for each event
```

---

## Advanced Usage

### Type-Safe Handler Protocol

You can use the `AsyncWebhookHandler` protocol for type hints:

```python
from zalobot_python import AsyncWebhookHandler, Context

# Type-annotated handler
my_handler: AsyncWebhookHandler = async def(ctx: Context) -> None:
    await ctx.reply("Hello!")
```

### Custom Secret Token

While the SDK generates secure tokens automatically, you can provide your own:

```python
bot = ZaloBot("token", _secret_token="your_custom_secret")
```

### Error Handling

```python
from zalobot_python import ZaloAPIError

try:
    await bot.sendMessage("chat_id", "Hello")
except ZaloAPIError as e:
    if e.error_code == 400:
        print("Bad request - invalid chat ID")
    else:
        print(f"API Error: {e.description}")
```

### Webhook Security

Always verify the secret token in your web server:

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    # Verify secret token
    if request.headers.get("X-Zalo-Secret-Token") != bot.get_secret_token():
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    event = Event.model_validate(await request.json())
    await bot.dispatch_webhook_handlers(event)
    return {"ok": True}
```

---

## License

MIT License
