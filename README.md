# WIP: Python SDK for the ZaloBot API

## Installation
For uv-astral  
```bash
uv add zalobot_python
```
For pip  
```bash
pip install zalobot_python
```

Usage
```python
import asyncio
from zalobot_python import ZaloBot, BotInfo 

bot = ZaloBot(BOT_TOKEN="<BOT TOKEN>")

async def main():
    bot_info: BotInfo = await bot.getMe()

    print(f"Bot ID: {bot_info.id}")
    print(f"Bot Name: {bot_info.display_name}")

asyncio.run(main())
```
