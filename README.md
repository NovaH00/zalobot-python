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

**Using uv:**
```bash
uv add zalobot-python
```

**Using pip:**
```bash
pip install zalobot-python
```

## API Coverage

| Method | Status |
|--------|--------|
| `getMe()` | ✅ |
| `getUpdates()` | ✅ |
| `setWebhook()` | ✅ |
| `deleteWebhook()` | ✅ |
| `getWebhookInfo()` | ✅ |
| `sendMessage()` | ✅ |
| `sendPhoto()` | Planned |
| `sendSticker()` | Planned |
| `sendChatAction()` | Planned |

## Quick Start

```python
import asyncio
from zalobot_python import ZaloBot

bot = ZaloBot("<BOT_TOKEN>")

async def main():
    bot_info = await bot.getMe()
    print(f"Bot: {bot_info.display_name}")

asyncio.run(main())
```

## Documentation

For comprehensive guides, API references, and examples, see the full documentation: **[Documentation](docs/DOCS.md)**

Topics covered in the docs:
- Detailed API reference with all methods and parameters
- Webhook vs Polling comparison
- Type-safe state management
- Error handling
- Advanced usage patterns
- Complete examples (Echo Bot, Command Handler, Multi-Handler Setup)

## License

MIT License
