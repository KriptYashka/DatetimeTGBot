import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union

import aiogram
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.command import CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import ForwardMessages
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InputFile, URLInputFile
from aiogram.utils.markdown import hbold

from resourses.text import CalcDatetimeText
from routers.admin.moderate_user import is_staff

router = Router(name=__name__)


# async def get_msg(url: str):
#     await bot.get_chat().

def str_to_datetime(s: str) -> Optional[datetime]:
    d, m, y = map(int, s.split("."))
    return datetime(y, m, d)


def get_timedelta_urls(*args) -> tuple[Optional[timedelta], str]:
    if len(args) != 2:
        return None, f"Количество аргументов должно быть 2. Проверьте пробелы.\nАргументы: {args}"
    try:
        date1 = str_to_datetime(args[0])
        date2 = str_to_datetime(args[1])
        return date2 - date1, "OK"
    except:
        return None, "Ошибка в дате. Формат: `/timedelta 31.12.2024 12.05.2025`"


@router.message(F.text.lower() == CalcDatetimeText.CALC_TEXT)
async def command_timedelta_handler(msg: Message) -> None:
    if not await is_staff(msg.from_user.username):
        await msg.reply(f"Функция недоступна")
        return

    # delta_date, status = get_timedelta_urls(*command.args.split())
    # if delta_date is not None:
    #     await msg.reply(f"Прошло {abs(delta_date.days)} дней")
    # else:
    #     await msg.reply(status)



# @router.message(Command("time"))
# async def command_timedelta_forward_handler(msg: Message, bot: aiogram.Bot):
#     messages = await bot.his


# async def command_timedelta_forward_first_handler(msg: list[Message], state: FSMContext):
#     date_str = msg.text
#     date2_str = await state.get_value("first")
#     print(date2_str)
#     if date2_str is None:
#         await state.update_data(first=date_str)
#         await msg.answer("Ожидание второго сообщения")
#         return
#     delta_date, status = get_timedelta_urls(date_str, date2_str)
#     if delta_date is not None:
#         await msg.reply(f"Прошло {abs(delta_date.days)} дней")
#         await state.clear()
#     else:
#         await msg.reply(status)
