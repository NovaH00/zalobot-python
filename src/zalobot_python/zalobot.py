from typing import Any, Literal
import httpx

from .models import (
    ZaloAPIResponse,
    SuccessfulResponse,
    ErrorResponse,
    ZaloAPIError,
    BotInfo,  
    WebhookInfo,
    MessageInfo,
    Event
)
from .config import ZaloAPIConfig

async def fetch[T](
    url: str,
    *,
    method: Literal["GET", "POST"] = "GET",
    body: dict[str, Any] | None = None,
) -> ZaloAPIResponse[T]:
    async with httpx.AsyncClient() as client:

        if method == "GET":
            response = await client.get(url)

        elif method == "POST":
            response = await client.post(url, json=body)

        response_json = response.json()

        if response_json.get("ok"):
            return SuccessfulResponse(**response_json)

        return ErrorResponse(**response_json)

class ZaloBot:
    def __init__(self, BOT_TOKEN: str):
        self._BOT_TOKEN: str = BOT_TOKEN
        self._base_url: str = f"{ZaloAPIConfig.BASE_URL}/bot{BOT_TOKEN}"
    
    async def getMe(self) -> BotInfo:
        url = f"{self._base_url}/getMe" 
        
        res: ZaloAPIResponse[BotInfo] = await fetch(url)
        
        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            ) 
        
       
        return res.result
                      
                
    async def getUpdates(self, timeout: int = 30) -> Event:
        url = f"{self._base_url}/getUpdates"
        
        payload = {
            "timeout": timeout
        }

        res: ZaloAPIResponse[Event] = await fetch(url, method="POST", body=payload)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def setWebhook(self, url: str, secret_token: str) -> WebhookInfo:
        url = f"{self._base_url}/setWebhook"
        
        payload = {
            "url": url,
            "secret_token": secret_token
        }

        res: ZaloAPIResponse[WebhookInfo] = await fetch(url, method="POST", body=payload)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result
    
    async def deleteWebhook(self) -> WebhookInfo:
        url = f"{self._base_url}/deleteWebhook"
        
        res: ZaloAPIResponse[WebhookInfo] = await fetch(url)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result

    async def getWebhookInfo(self) -> WebhookInfo:
        url = f"{self._base_url}/getWebhookInfo"
        
        res: ZaloAPIResponse[WebhookInfo] = await fetch(url)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result
    
    async def sendMessage(self, chat_id: str, text: str) -> MessageInfo:
        url = f"{self._base_url}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        res: ZaloAPIResponse[MessageInfo] = await fetch(url, method="POST", body=payload)

        if isinstance(res, ErrorResponse):
            raise ZaloAPIError(
                res.error_code,
                res.description
            )

        return res.result


    async def sendPhoto(self, chat_id: str, caption: str, photo_url: str) -> None:
        raise NotImplementedError()

    async def sendSticker(self, chat_id: str, sticker: str) -> None:
        raise NotImplementedError()

    async def sendChatAction(self, chat_id: str, action: str) -> None:
        raise NotImplementedError()
