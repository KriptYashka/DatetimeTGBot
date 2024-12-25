from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from routers.datetime_calc import router as r_calc
from routers.datetime_msg import router as r_calc_msg
from routers.admin.moderate_user import router as r_admin
from routers.common import router as r_common

def create_dispatcher():
    dp = Dispatcher()
    dp.include_router(r_calc)
    dp.include_router(r_calc_msg)
    dp.include_router(r_admin)
    dp.include_router(r_common)
    return dp



# # Примеры команд. TODO: Будут перенесены в другую папку
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     """
#     Обработчик команды `/start`.
#     """
#     await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
#
#
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Обработчик перенаправит полученное сообщение обратно отправителю.
#
#     По умолчанию обработчик сообщений обрабатывает все типы сообщений (например, текст, фотографию, стикер и т. д.).
#     """
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")