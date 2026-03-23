from typing import final 
from ..types import Event, EventName, MessageInfo, From, Chat
from .interfaces import ZaloBotAPI

@final
class Context:
    def __init__(self, *, _update: Event, _bot: ZaloBotAPI):
        self._update = _update
        self._bot = _bot

    async def reply(self, text: str) -> MessageInfo:
        return await self._bot.sendMessage(self.chat_id, text) 

    @property
    def chat_id(self) -> str:
        return self._update.message.chat.id 

    @property
    def user_id(self) -> str:
        return self._update.message.sender.id

    @property
    def text(self) -> str:
        return self._update.message.text

    @property
    def message_id(self) -> str:
        return self._update.message.message_id

    @property
    def sender(self) -> From:
        return self._update.message.sender
    
    @property
    def chat(self) -> Chat:
        return self._update.message.chat

    @property
    def is_text(self) -> bool:
        return self._update.event_name == EventName.TEXT_RECEIVED 

    @property
    def is_image(self) -> bool:
        return self._update.event_name == EventName.IMAGE_RECEIVED

    @property
    def is_sticker(self) -> bool:
        return self._update.event_name == EventName.STICKER_RECEIVED

    @property
    def is_unsupported(self) -> bool:
        return self._update.event_name == EventName.UNSUPPORTED_RECEIVED
