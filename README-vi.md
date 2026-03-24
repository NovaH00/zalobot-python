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

**Sử dụng uv:**
```bash
uv add zalobot-python
```

**Sử dụng pip:**
```bash
pip install zalobot-python
```

## API Hỗ Trợ

| Phương thức | Trạng thái |
|-------------|------------|
| `getMe()` | ✅ |
| `getUpdates()` | ✅ |
| `setWebhook()` | ✅ |
| `deleteWebhook()` | ✅ |
| `getWebhookInfo()` | ✅ |
| `sendMessage()` | ✅ |
| `sendPhoto()` | Theo kế hoạch |
| `sendSticker()` | Theo kế hoạch |
| `sendChatAction()` | Theo kế hoạch |

## Bắt Đầu Nhanh

```python
import asyncio
from zalobot_python import ZaloBot

bot = ZaloBot("<BOT_TOKEN>")

async def main():
    bot_info = await bot.getMe()
    print(f"Bot: {bot_info.display_name}")

asyncio.run(main())
```

## Tài Liệu

Để biết hướng dẫn chi tiết, API reference và ví dụ, xem tài liệu đầy đủ: **[Documentation](docs/DOCS-vi.md)**

Các nội dung trong tài liệu:
- API reference chi tiết với tất cả phương thức và tham số
- So sánh Webhook vs Polling
- Quản lý trạng thái type-safe
- Xử lý lỗi
- Các mẫu sử dụng nâng cao
- Ví dụ hoàn chỉnh (Echo Bot, Command Handler, Multi-Handler Setup)

## License

MIT License
