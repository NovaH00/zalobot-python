[Tiếng Việt](README-vi.md)
# ZaloBot Python SDK (Work in Progress)

A modern, fully-typed, and asynchronous Python SDK for the ZaloBot API. This library was built as a more ergonomic and developer-friendly alternative to the official SDK.

## Features

| Feature | Description |
|---------|-------------|
| **Fully Typed & Documented** | Complete type hints and docstrings. No need to dig through source code to figure out expected data types. |
| **Pydantic Data Modeling** | All API responses are validated and converted into Pydantic models. This improves Developer Experience (DX) and significantly reduces errors related to raw JSON parsing. |
| **True Asynchronous Execution** | Non-blocking async operations designed to avoid runtime errors, even when used within applications where the main thread is fully occupied. |
| **Ergonomic Webhooks** | Simplified webhook configuration and event dispatching mechanisms. |

## Installation

You can install the SDK using your preferred package manager:

**Using uv:**
~~~bash
uv add zalobot_python
~~~

**Using pip:**
~~~bash
pip install zalobot_python
~~~

## API Coverage

Methods formatted in `camelCase` directly map to the equivalent Zalo API endpoints.

| Method | Zalo Endpoint | Status |
|--------|---------------|--------|
| `getMe()` | `/getMe` | Implemented |
| `getUpdates()` | `/getUpdates` | Implemented |
| `setWebhook()` | `/setWebhook` | Implemented |
| `deleteWebhook()` | `/deleteWebhook` | Implemented |
| `getWebhookInfo()` | `/getWebhookInfo` | Implemented |
| `sendMessage()` | `/sendMessage` | Implemented |
| `sendPhoto()` | `/sendPhoto` | Planned |
| `sendSticker()` | `/sendSticker` | Planned |
| `sendChatAction()` | `/sendChatAction` | Planned |

## Usage

### Basic Usage

The simplest way to use the bot is to instantiate it with your token and call the available endpoint methods.

~~~python
import asyncio
from zalobot_python import ZaloBot, BotInfo 

bot = ZaloBot(BOT_TOKEN="<BOT_TOKEN>")

async def main():
    bot_info: BotInfo = await bot.getMe()
    
    print(f"Bot ID: {bot_info.id}")
    print(f"Bot Name: {bot_info.display_name}")

if __name__ == "__main__":
    asyncio.run(main())
~~~

### Webhook Usage

While you can technically poll `.getUpdates()` to receive new events, using a webhook is significantly more efficient. The SDK provides built-in mechanisms to easily configure and handle webhooks.

~~~python
from zalobot_python import ZaloBot, Context, AsyncWebhookHandler, ZaloAPIResponse, Event 

# 1. Initialize the standard bot
normal_bot = ZaloBot("<BOT_TOKEN>")

# 2. Define your webhook handlers
async def echo(ctx: Context):
    message_info = await ctx.reply(f"You sent: {ctx.text}")
    print("Sent message ID:", message_info.message_id)

async def log_event(ctx: Context):
    if ctx.is_text:
        print("Chat ID:", ctx.chat_id)
        print("Message:", ctx.text)

async def main():
    # Convert the standard bot into a webhook-enabled bot
    # (All previously available endpoint methods remain usable)
    webhook_bot = await normal_bot.configure_webhook("https://your-domain.com/webhook")
    
    # Retrieve the auto-generated secret token. 
    # Use this to validate the X-Bot-Api-Secret-Token header in incoming requests.
    secret_token = webhook_bot.get_secret_token() 
    
    # Register handlers
    webhook_bot.add_webhook_handler(echo)
    webhook_bot.add_webhook_handler(log_event)

    # Note: The request handling flow below should be implemented 
    # inside your web framework's endpoint (e.g., FastAPI, Flask).
~~~

#### Request Handling Flow (For Web Frameworks)

When implementing the actual route in your web framework, follow these steps to process incoming events:

1. **Parse the payload:** Parse the incoming JSON body into a `ZaloAPIResponse[Event]`. The actual payload resides in the `result` field.
~~~python
parsed: ZaloAPIResponse[Event] = ZaloAPIResponse.model_validate(request.json())
~~~

2. **Extract the event:**
~~~python
event = parsed.result
~~~

3. **Dispatch the event:** Pass the event to your registered handlers.
~~~python
await webhook_bot.dispatch_webhook_handlers(event)
~~~

## Architecture Note: Webhook State Management

To ensure strict type safety, the `ZaloBot` class is a generic that relies on two specific states: 

| State | Description |
|-------|-------------|
| `UnconfiguredWebhook` | The default state when `ZaloBot` is instantiated. |
| `ConfiguredWebhook` | The state returned after calling `.configure_webhook()`. |

**Why does this matter?**
All helper methods written in `snake_case` (such as `add_webhook_handler`) are specific to webhook operations. Because of the generic state design, static analyzers (like Pyright or MyPy) will flag an error if you attempt to call a `snake_case` method on an unconfigured bot (`ZaloBot[UnconfiguredWebhook]`). These methods are only exposed and valid on instances of `ZaloBot[ConfiguredWebhook]`.
