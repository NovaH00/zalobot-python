from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, Header, HTTPException, status
from zalobot_python import ZaloBot, ConfiguredWebhook, Context, Event

async def command_handler(ctx: Context):
    """Handle commands that start with /"""
    if not ctx.is_text or not ctx.text.startswith("/"):
        return

    command = ctx.text.split()[0].lower()  # Get first word (command)
    args = ctx.text.split()[1:]  # Get remaining arguments

    if command == "/start":
        await ctx.reply(
            "Welcome! I'm a command bot.\n\n"
            "Available commands:\n"
            "/start - Show this welcome message\n"
            "/time - Show current time\n"
            "/date - Show current date\n"
            "/datetime - Show current date and time\n"
            "/echo <text> - Echo your message"
        )

    elif command == "/time":
        current_time = datetime.now().strftime("%H:%M:%S")
        await ctx.reply(f"Current time: {current_time}")

    elif command == "/date":
        current_date = datetime.now().strftime("%Y-%m-%d")
        await ctx.reply(f"Current date: {current_date}")

    elif command == "/datetime":
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await ctx.reply(f"Current date and time: {current_datetime}")

    elif command == "/echo":
        if args:
            await ctx.reply(" ".join(args))
        else:
            await ctx.reply("Please provide text to echo. Usage: /echo <text>")

    elif command == "/help":
        await ctx.reply(
            "Help\n\n"
            "Send /start to see available commands."
        )

    else:
        await ctx.reply(f"Unknown command: {command}\n\nSend /start to see available commands.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    normal_bot = ZaloBot("<BOT TOKEN>")
    webhook_bot = await normal_bot.configure_webhook("https://your-domain.com/webhook")
    webhook_bot.add_webhook_handler(command_handler)
    app.state.zalobot = webhook_bot

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(
    request: Request,
    x_bot_api_secret_token: str = Header()
):
    zalobot: ZaloBot[ConfiguredWebhook] = request.app.state.zalobot

    if x_bot_api_secret_token != zalobot.get_secret_token():
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect secret"
        )

    data = await request.json()
    event = Event.model_validate(data)

    await zalobot.dispatch_webhook_handlers(event)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080
    )
