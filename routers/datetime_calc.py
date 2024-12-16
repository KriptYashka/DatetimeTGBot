from typing import Any

from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)

@router.message()
async def message_handler(message: Message) -> Any:
    await message.answer('Hello from my router!')