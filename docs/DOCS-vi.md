# Tài Liệu ZaloBot Python SDK

Một Python SDK hiện đại, đầy đủ type, và bất đồng bộ cho Zalo Bot API.

## Mục Lục

- [Tổng Quan](#tổng-quan)
- [Cài Đặt](#cài-đặt)
- [Bắt Đầu Nhanh](#bắt-đầu-nhanh)
- [Khái Niệm Cốt Lõi](#khái-niệm-cốt-lõi)
  - [Trạng Thái Bot](#trạng-thái-bot)
  - [Webhook vs Polling](#webhook-vs-polling)
- [API Reference](#api-reference)
  - [ZaloBot](#zalobot)
  - [Context](#context)
  - [Types](#types)
  - [Errors](#errors)
- [Ví Dụ](#ví-dụ)
- [Sử Dụng Nâng Cao](#sử-dụng-nâng-cao)

---

## Tổng Quan

ZaloBot Python là một SDK do cộng đồng xây dựng, cung cấp giao diện an toàn về kiểu và dễ sử dụng để phát triển chatbot Zalo. Các tính năng chính:

- **Fully Typed**: Đầy đủ type hints để hỗ trợ IDE tốt hơn và phát hiện lỗi sớm
- **Asynchronous**: Xây dựng trên `asyncio` và `httpx` cho I/O không chặn
- **Type-Safe States**: Generic types ngăn chặn chuyển trạng thái không hợp lệ
- **Pydantic Models**: Tất cả dữ liệu API được validate bằng Pydantic
- **Ergonomic Design**: API sạch, trực quan, lấy cảm hứng từ các framework bot hiện đại

---

## Cài Đặt

Cài đặt bằng `uv`:

```bash
uv add zalobot-python
```

Hoặc sử dụng `pip`:

```bash
pip install zalobot-python
```

### Yêu Cầu

- Python 3.12+
- `httpx` cho HTTP requests
- `pydantic` cho data validation

---

## Bắt Đầu Nhanh

### 1. Tạo Bot Instance

```python
from zalobot_python import ZaloBot

bot = ZaloBot("your_bot_token_here")
```

### 2. Lấy Thông Tin Bot

```python
bot_info = await bot.getMe()
print(f"Tên bot: {bot_info.display_name}")
```

### 3. Thiết Lập Webhook (Khuyến Nghị Cho Production)

```python
from zalobot_python import Context

async def echo_handler(ctx: Context):
    """Phản hồi lại mọi tin nhắn văn bản"""
    if ctx.is_text:
        await ctx.reply(f"Bạn nói: {ctx.text}")

# Cấu hình webhook
configured_bot = await bot.configure_webhook("https://your-domain.com/webhook")

# Đăng ký handler
configured_bot.add_webhook_handler(echo_handler)

# Trong web server của bạn, khi nhận webhook event:
# await configured_bot.dispatch_webhook_handlers(event)
```

### 4. Sử Dụng Polling (Cho Phát Triển)

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

## Khái Niệm Cốt Lõi

### Trạng Thái Bot

SDK sử dụng pattern type-state để ngăn chặn các thao tác không hợp lệ:

- **`UnconfiguredWebhook`**: Trạng thái ban đầu. Bot có thể dùng polling hoặc cấu hình webhook.
- **`ConfiguredWebhook`**: Sau khi webhook được cấu hình. Bot có thể xử lý webhook events.

```python
bot = ZaloBot("token")  # Type: ZaloBot[UnconfiguredWebhook]

# Hợp lệ - chuyển từ UnconfiguredWebhook sang ConfiguredWebhook
configured_bot = await bot.configure_webhook("https://example.com")  # Type: ZaloBot[ConfiguredWebhook]

# Lỗi type - setWebhook chỉ hoạt động trên UnconfiguredWebhook
# await configured_bot.setWebhook(...)  # Type checker sẽ bắt lỗi này!
```

### Webhook vs Polling

| Tính Năng | Webhook | Polling |
|-----------|---------|---------|
| **Hiệu Suất** | Real-time, push-based | Trễ, pull-based |
| **Tài Nguyên** | Thấp (chỉ khi có event) | Cao (polling liên tục) |
| **Độ Phức Tạp** | Cần HTTPS server | Đơn giản, không cần server |
| **Phù Hợp** | Production | Development/Testing |

---

## API Reference

### ZaloBot

Class chính để tương tác với Zalo Bot API.

#### Constructor

```python
ZaloBot(BOT_TOKEN: str, *, _secret_token: str | None = None)
```

- `BOT_TOKEN`: Token bot từ Zalo Bot Platform
- `_secret_token`: Dùng nội bộ, tự động thiết lập bởi `configure_webhook()`

#### Methods

##### `getMe() -> BotInfo`

Lấy thông tin về bot.

**Trả Về:** Thông tin bot bao gồm ID, tên, và capabilities

**Ví dụ:**
```python
info = await bot.getMe()
print(f"Bot: {info.display_name}, Có thể vào nhóm: {info.can_join_groups}")
```

##### `getUpdates(timeout: int = 30) -> Event`

Poll cho updates mới sử dụng long polling.

**Tham Số:**
- `timeout`: Số giây tối đa chờ updates (mặc định: 30)

**Trả Về:** Event mới nhất

**Ví dụ:**
```python
event = await bot.getUpdates(timeout=30)
print(f"Loại event: {event.event_name}")
```

##### `setWebhook(webhook_url: str, secret_token: str) -> WebhookInfo`

Thiết lập URL webhook để nhận updates.

**Tham Số:**
- `webhook_url`: URL HTTPS để nhận webhook events
- `secret_token`: Secret token để xác thực webhook

**Trả Về:** Thông tin cấu hình webhook

**Lưu ý:** Chỉ khả dụng trên `ZaloBot[UnconfiguredWebhook]`

##### `deleteWebhook() -> WebhookInfo`

Xóa cấu hình webhook hiện tại.

**Trả Về:** WebhookInfo với URL rỗng và timestamp hiện tại

**Lưu ý:** Không giống một số API, phương thức này vẫn thành công ngay cả khi không có
webhook nào được cấu hình. API trả về WebhookInfo với giá trị rỗng/mặc định thay vì
thông tin về webhook đã xóa.

**Ví dụ:**
```python
# Xóa webhook an toàn (ngay cả khi không có webhook)
await bot.deleteWebhook()
```

##### `getWebhookInfo() -> WebhookInfo`

Lấy cấu hình webhook hiện tại.

**Trả Về:** URL webhook và trạng thái

##### `sendMessage(chat_id: str, text: str) -> MessageInfo`

Gửi tin nhắn văn bản đến một chat.

**Tham Số:**
- `chat_id`: Định danh duy nhất của chat
- `text`: Nội dung tin nhắn

**Trả Về:** Thông tin về tin nhắn đã gửi

**Ví dụ:**
```python
result = await bot.sendMessage("chat_123", "Xin chào!")
print(f"Message ID: {result.message_id}")
```

##### `sendPhoto(chat_id: str, caption: str, photo_url: str) -> None`

Gửi ảnh đến một chat.

**Trạng Thái:** Chưa được triển khai

##### `sendSticker(chat_id: str, sticker: str) -> None`

Gửi sticker đến một chat.

**Trạng Thái:** Chưa được triển khai

##### `sendChatAction(chat_id: str, action: str) -> None`

Gửi chat action (ví dụ: đang gõ).

**Trạng Thái:** Chưa được triển khai

##### `configure_webhook(url: str) -> ZaloBot[ConfiguredWebhook]`

Cấu hình webhook và trả về bot instance mới ở trạng thái configured.

**Tham Số:**
- `url`: URL HTTPS cho webhook events

**Trả Về:** `ZaloBot` instance mới ở trạng thái `ConfiguredWebhook`

**Lưu ý:** Phương thức này đầu tiên gọi `deleteWebhook()` để đảm bảo trạng thái
sạch trước khi thiết lập webhook mới. Điều này ngăn lỗi nếu webhook đã được cấu
hình trước đó.

**Cảnh Báo:** Ném `ZaloAPIError` nếu Zalo API không thể thiết lập webhook.

**Ví dụ:**
```python
configured_bot = await bot.configure_webhook("https://example.com/webhook")
```

##### `get_secret_token() -> str`

Lấy secret token để xác thực webhook.

**Trả Về:** Secret token string

**Lưu ý:** Chỉ khả dụng trên `ZaloBot[ConfiguredWebhook]`

##### `add_webhook_handler(handler: AsyncWebhookHandler) -> None`

Đăng ký handler function cho webhook events.

**Tham Số:**
- `handler`: Async function nhận `Context` object

**Ví dụ:**
```python
async def handler(ctx: Context):
    await ctx.reply("Xin chào!")

bot.add_webhook_handler(handler)
```

##### `dispatch_webhook_handlers(update_event: Event) -> None`

Dispatch event đến tất cả handlers đã đăng ký.

**Tham Số:**
- `update_event`: Event nhận từ webhook

**Lưu ý:** Được gọi nội bộ bởi web server của bạn

---

### Context

Context object được truyền cho webhook handlers, cung cấp truy cập vào event data và methods phản hồi.

#### Properties

| Property | Type | Mô Tả |
|----------|------|-------|
| `chat_id` | `str` | ID của chat hiện tại |
| `user_id` | `str` | ID của người gửi tin nhắn |
| `text` | `str` | Nội dung văn bản của tin nhắn |
| `message_id` | `str` | Định danh tin nhắn duy nhất |
| `sender` | `From` | Object thông tin người gửi |
| `chat` | `Chat` | Object thông tin chat |
| `is_text` | `bool` | True nếu tin nhắn là văn bản |
| `is_image` | `bool` | True nếu tin nhắn là ảnh |
| `is_sticker` | `bool` | True nếu tin nhắn là sticker |
| `is_unsupported` | `bool` | True nếu loại tin nhắn không hỗ trợ |

#### Methods

##### `reply(text: str) -> MessageInfo`

Phản hồi lại tin nhắn hiện tại.

**Tham Số:**
- `text`: Nội dung tin nhắn phản hồi

**Trả Về:** Thông tin về tin nhắn phản hồi đã gửi

**Ví dụ:**
```python
async def handler(ctx: Context):
    await ctx.reply("Cảm ơn tin nhắn của bạn!")
```

---

### Types

#### BotInfo

Model thông tin bot.

**Fields:**
- `id`: Định danh duy nhất của bot
- `account_name`: Tên tài khoản
- `account_type`: Loại tài khoản (ví dụ: "official")
- `can_join_groups`: Bot có thể vào nhóm không
- `display_name`: Tên hiển thị cho người dùng

#### WebhookInfo

Thông tin cấu hình webhook.

**Fields:**
- `url`: URL webhook đã cấu hình
- `updated_at`: Unix timestamp của lần cập nhật cuối

#### MessageInfo

Kết quả gửi tin nhắn.

**Fields:**
- `message_id`: ID tin nhắn đã gửi
- `date`: Unix timestamp của thời điểm gửi

#### Event

Webhook event đầu vào.

**Fields:**
- `event_name`: Loại event (`EventName` enum)
- `message`: Object message

#### EventName

Enumeration của các loại event:

- `TEXT_RECEIVED` - "message.text.received"
- `IMAGE_RECEIVED` - "message.image.received"
- `STICKER_RECEIVED` - "message.sticker.received"
- `UNSUPPORTED_RECEIVED` - "message.unsupported.received"

#### From

Thông tin người gửi.

**Fields:**
- `id`: User ID
- `display_name`: Tên hiển thị của user
- `is_bot`: Người gửi có phải là bot không

#### Chat

Thông tin chat.

**Fields:**
- `id`: Chat ID
- `chat_type`: Loại chat (ví dụ: "private", "group")

#### Message

Object message.

**Fields:**
- `sender`: Thông tin người gửi (`From`)
- `chat`: Thông tin chat (`Chat`)
- `text`: Nội dung tin nhắn
- `message_id`: ID tin nhắn
- `date`: Unix timestamp

---

### Errors

#### ZaloAPIError

Exception được ném khi Zalo API trả về lỗi.

**Attributes:**
- `error_code`: Mã lỗi số
- `description`: Mô tả lỗi dễ đọc

**Ví dụ:**
```python
try:
    await bot.sendMessage("invalid", "Xin chào")
except ZaloAPIError as e:
    print(f"Lỗi {e.error_code}: {e.description}")
```

---

## Ví Dụ

### Echo Bot (Webhook)

```python
from zalobot_python import ZaloBot, Context

async def echo_handler(ctx: Context):
    if ctx.is_text:
        await ctx.reply(f"Echo: {ctx.text}")

bot = ZaloBot("your_token")
configured_bot = await bot.configure_webhook("https://your-domain.com/webhook")
configured_bot.add_webhook_handler(echo_handler)

# Trong web server (ví dụ: FastAPI):
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
            await ctx.reply("Chào mừng! Hãy gửi tin nhắn cho tôi.")
        elif text == "/help":
            await ctx.reply("Tôi có thể echo tin nhắn của bạn!")
        elif text.startswith("/echo "):
            await ctx.reply(text[6:])  # Xóa tiền tố "/echo "

bot = ZaloBot("token")
configured_bot = await bot.configure_webhook("https://example.com/webhook")
configured_bot.add_webhook_handler(command_handler)
```

### Multi-Handler Setup

```python
from zalobot_python import Context

async def log_handler(ctx: Context):
    print(f"Tin nhắn từ {ctx.sender.display_name}: {ctx.text}")

async def response_handler(ctx: Context):
    if ctx.is_text:
        await ctx.reply("Tôi đã nhận được tin nhắn của bạn!")

bot = ZaloBot("token")
configured_bot = await bot.configure_webhook("https://example.com/webhook")
configured_bot.add_webhook_handler(log_handler)
configured_bot.add_webhook_handler(response_handler)
# Cả hai handlers sẽ được gọi cho mỗi event
```

---

## Sử Dụng Nâng Cao

### Type-Safe Handler Protocol

Bạn có thể sử dụng protocol `AsyncWebhookHandler` cho type hints:

```python
from zalobot_python import AsyncWebhookHandler, Context

# Handler với type annotation
my_handler: AsyncWebhookHandler = async def(ctx: Context) -> None:
    await ctx.reply("Xin chào!")
```

### Custom Secret Token

Mặc dù SDK tự động tạo token an toàn, bạn có thể cung cấp token riêng:

```python
bot = ZaloBot("token", _secret_token="your_custom_secret")
```

### Xử Lý Lỗi

```python
from zalobot_python import ZaloAPIError

try:
    await bot.sendMessage("chat_id", "Xin chào")
except ZaloAPIError as e:
    if e.error_code == 400:
        print("Bad request - chat ID không hợp lệ")
    else:
        print(f"Lỗi API: {e.description}")
```

### Bảo Mật Webhook

Luôn xác thực secret token trong web server của bạn:

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    # Xác thực secret token
    if request.headers.get("X-Zalo-Secret-Token") != bot.get_secret_token():
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    event = Event.model_validate(await request.json())
    await bot.dispatch_webhook_handlers(event)
    return {"ok": True}
```

---

## Giấy Phép 

MIT 
