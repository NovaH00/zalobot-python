[English](README.md)
# ZaloBot Python SDK (Đang phát triển)

SDK Python hiện đại, fully-typed và asynchronous cho Zalo Bot API. 

## Tính năng

| Tính năng | Mô tả |
|---------|-------------|
| **Định kiểu đầy đủ & Có tài liệu rõ ràng** | Đầy đủ type hints và docstrings. Không cần phải đọc sâu vào mã nguồn để biết kiểu dữ liệu nào đang được sử dụng. |
| **Mô hình hóa dữ liệu với Pydantic** | Tất cả các phản hồi từ API đều được xác thực và chuyển đổi thành các mô hình Pydantic. Điều này giúp cải thiện Trải nghiệm Lập trình viên (DX) và giảm thiểu các lỗi tiềm ẩn khi xử lý JSON thuần túy. |
| **Thực thi bất đồng bộ thực sự** | Các hoạt động async không chặn (non-blocking) được thiết kế để không gây ra lỗi runtime, ngay cả khi bạn sử dụng trong một ứng dụng mà luồng chính (main thread) đã bị chiếm dụng hoàn toàn. |
| **Webhook tiện dụng** | Các cơ chế cấu hình webhook và điều phối sự kiện được đơn giản hóa tối đa. |

## Cài đặt

Bạn có thể cài đặt SDK bằng trình quản lý gói ưa thích của mình:

**Sử dụng uv:**
~~~bash
uv add zalobot_python
~~~

**Sử dụng pip:**
~~~bash
pip install zalobot_python
~~~

## Các API hỗ trợ

Các phương thức được viết theo định dạng `camelCase` sẽ thực hiện các lệnh gọi API tương đương đến các endpoint của Zalo:

| Phương thức | Endpoint Zalo | Trạng thái |
|--------|---------------|--------|
| `getMe()` | `/getMe` | Đã hoàn thiện |
| `getUpdates()` | `/getUpdates` | Đã hoàn thiện |
| `setWebhook()` | `/setWebhook` | Đã hoàn thiện |
| `deleteWebhook()` | `/deleteWebhook` | Đã hoàn thiện |
| `getWebhookInfo()` | `/getWebhookInfo` | Đã hoàn thiện |
| `sendMessage()` | `/sendMessage` | Đã hoàn thiện |
| `sendPhoto()` | `/sendPhoto` | Theo kế hoạch |
| `sendSticker()` | `/sendSticker` | Theo kế hoạch |
| `sendChatAction()` | `/sendChatAction` | Theo kế hoạch |

## Cách sử dụng

### Sử dụng cơ bản

Cách đơn giản nhất để sử dụng bot là khởi tạo bot với token của bạn và gọi các phương thức endpoint có sẵn.

~~~python
import asyncio
from zalobot_python import ZaloBot, BotInfo 

bot = ZaloBot(BOT_TOKEN="<BOT_TOKEN>")

async def main():
    bot_info: BotInfo = await bot.getMe()
    
    print(f"ID Bot: {bot_info.id}")
    print(f"Tên Bot: {bot_info.display_name}")

if __name__ == "__main__":
    asyncio.run(main())
~~~

### Sử dụng Webhook

Mặc dù về mặt kỹ thuật, bạn có thể liên tục gọi `.getUpdates()` (polling) để nhận các sự kiện mới, nhưng sử dụng webhook sẽ hiệu quả hơn nhiều. SDK cung cấp sẵn các cơ chế tích hợp để dễ dàng cấu hình và xử lý webhook.

~~~python
from zalobot_python import ZaloBot, Context, AsyncWebhookHandler, ZaloAPIResponse, Event 

# 1. Khởi tạo bot tiêu chuẩn
normal_bot = ZaloBot("<BOT_TOKEN>")

# 2. Định nghĩa các hàm xử lý (handler) cho webhook
async def echo(ctx: Context):
    message_info = await ctx.reply(f"Bạn đã gửi: {ctx.text}")
    print("ID tin nhắn đã gửi:", message_info.message_id)

async def log_event(ctx: Context):
    if ctx.is_text:
        print("ID Cuộc trò chuyện:", ctx.chat_id)
        print("Tin nhắn:", ctx.text)

async def main():
    # Chuyển đổi bot tiêu chuẩn thành bot hỗ trợ webhook
    # (Tất cả các phương thức endpoint có sẵn trước đó vẫn sử dụng được bình thường)
    webhook_bot = await normal_bot.configure_webhook("https://your-domain.com/webhook")
    
    # Lấy secret token được tạo tự động. 
    # Sử dụng token này để xác thực header X-Bot-Api-Secret-Token trong các request gửi đến.
    secret_token = webhook_bot.get_secret_token() 
    
    # Đăng ký các hàm xử lý
    webhook_bot.add_webhook_handler(echo)
    webhook_bot.add_webhook_handler(log_event)

    # Lưu ý: Luồng xử lý request bên dưới cần được triển khai 
    # bên trong endpoint của web framework bạn đang dùng (VD: FastAPI, Flask).
~~~

#### Luồng xử lý yêu cầu (Dành cho Web Framework)

Khi triển khai route thực tế trong web framework, hãy làm theo các bước sau để xử lý các sự kiện gửi đến:

1. **Phân tích cú pháp payload:** Chuyển đổi phần thân JSON gửi đến thành đối tượng `ZaloAPIResponse[Event]`. Payload thực tế nằm trong trường `result`.
~~~python
parsed: ZaloAPIResponse[Event] = ZaloAPIResponse.model_validate(request.json())
~~~

2. **Trích xuất sự kiện (event):**
~~~python
event = parsed.result
~~~

3. **Điều phối sự kiện:** Truyền sự kiện tới các hàm xử lý đã đăng ký của bạn.
~~~python
await webhook_bot.dispatch_webhook_handlers(event)
~~~

## Lưu ý về Kiến trúc: Quản lý trạng thái Webhook

Để đảm bảo an toàn kiểu dữ liệu (type safety) một cách nghiêm ngặt, lớp `ZaloBot` là một lớp generic (generic class) phụ thuộc vào hai trạng thái cụ thể:

| Trạng thái | Mô tả |
|-------|-------------|
| `UnconfiguredWebhook` | Trạng thái mặc định khi `ZaloBot` được khởi tạo. |
| `ConfiguredWebhook` | Trạng thái được trả về sau khi gọi phương thức `.configure_webhook()`. |

**Tại sao điều này lại quan trọng?**
Tất cả các phương thức hỗ trợ được viết dưới dạng `snake_case` (ví dụ như `add_webhook_handler`) đều dành riêng cho các hoạt động của webhook. Nhờ thiết kế trạng thái generic này, các công cụ phân tích tĩnh (như Pyright hay MyPy) sẽ báo lỗi nếu bạn cố gọi một phương thức `snake_case` trên một bot chưa được cấu hình (`ZaloBot[UnconfiguredWebhook]`). Các phương thức này chỉ được hiển thị và hợp lệ trên các thực thể của `ZaloBot[ConfiguredWebhook]`.
