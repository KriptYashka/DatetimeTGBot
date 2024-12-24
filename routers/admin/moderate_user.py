import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union
from aiogram.filters import CommandStart, Command
from aiogram.filters.command import CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import ForwardMessages
from aiogram.types import Message

from aiogram import Router
from aiogram.filters import Command

from models import UserOrm
from repositories import UserRepository

router = Router(name=__name__)

async def is_staff(tg_id: str):
    user = await UserRepository.get_user_by_tg_id(tg_id)
    if user is None:
        return None
    return user.is_staff

# def decorator_factory(argument):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             funny_stuff()
#             something_with_argument(argument)
#             result = function(*args, **kwargs)
#             more_funny_stuff()
#             return result
#         return wrapper
#     return decorator

@router.message(Command("add_moderator"))
async def command_add_moderator_handler(msg: Message, command: CommandObject):
    tg_id = command.args.replace("@", "")

    # TODO: В отдельный обработчик
    data = {
        "tg_id": tg_id,
        "datetime_register": datetime.now(),
        "is_staff": True
    }
    user = UserOrm(**data)
    await UserRepository.create_user(user)

    await msg.reply("Пользователь добавлен модератором")

