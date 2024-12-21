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
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InputFile, URLInputFile
from aiogram.utils.markdown import hbold

router = Router(name=__name__)

# async def get_msg(url: str):
#     await bot.get_chat().

async def get_timedelta_urls(args) -> tuple[Optional[timedelta], str]:
    args = args.split()
    if len(args) != 2:
        return None, f"Количество аргументов должно быть 2. Проверьте пробелы.\nАргументы: {args}"
    try:
        d1, m1, y1 = map(int, args[0].split("."))
        d2, m2, y2 = map(int, args[1].split("."))
        date1 = datetime(y1, m1, d1)
        date2 = datetime(y2, m2, d2)
        return date2-date1, "OK"
    except:
        return None, "Ошибка в дате. Формат: `/timedelta 31.12.2024 12.05.2025`"


@router.message(Command("timedelta"))
async def command_timedelta_handler(msg: Message, bot: aiogram.Bot, command: CommandObject) -> None:
    delta_date, status = await get_timedelta_urls(command.args)
    if delta_date is not None:
        await msg.reply(f"Прошло {abs(delta_date.days)} дней")
    else:
        await msg.reply(status)