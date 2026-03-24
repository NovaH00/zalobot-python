from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Header, HTTPException, status
from zalobot_python import ZaloBot, ConfiguredWebhook, Context, Event

async def echo_handler(ctx: Context):
    message_info = await ctx.reply(f"You sent: {ctx.text}")
    print("Echo to message_id:", message_info.message_id)

@asynccontextmanager
async def lifespan(app: FastAPI):
    normal_bot = ZaloBot("<BOT TOKEN>")
    webhook_bot = await normal_bot.configure_webhook("https://your-domain.com/webhook")
    webhook_bot.add_webhook_handler(echo_handler)
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
