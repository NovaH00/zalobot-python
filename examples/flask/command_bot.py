from contextlib import asynccontextmanager
from datetime import datetime

from flask import Flask, request, jsonify, abort
from zalobot_python import ZaloBot, Context, Event

app = Flask(__name__)

# Initialize bot and configure webhook
normal_bot = ZaloBot("<BOT TOKEN>")
webhook_bot = None
secret_token = None

def init_bot():
    global webhook_bot, secret_token
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    webhook_bot = loop.run_until_complete(normal_bot.configure_webhook("https://your-domain.com/webhook"))
    secret_token = webhook_bot.get_secret_token()
    webhook_bot.add_webhook_handler(command_handler)

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

@app.post("/webhook")
def webhook():
    # Verify secret token
    x_bot_api_secret_token = request.headers.get("X-Bot-Api-Secret-Token")
    if not x_bot_api_secret_token or x_bot_api_secret_token != secret_token:
        abort(401, description="Incorrect secret")

    data = request.get_json()
    event = Event.model_validate(data)

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(webhook_bot.dispatch_webhook_handlers(event))

    return jsonify({"ok": True})

if __name__ == "__main__":
    init_bot()
    app.run(
        host="0.0.0.0",
        port=8080
    )
