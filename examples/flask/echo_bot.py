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
    webhook_bot.add_webhook_handler(echo_handler)

async def echo_handler(ctx: Context):
    message_info = await ctx.reply(f"You sent: {ctx.text}")
    print("Echo to message_id:", message_info.message_id)

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
