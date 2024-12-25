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

from resourses.text import CalcDatetimeText, AdminText
from routers.admin.moderate_user import is_staff
from routers.keyboard.keyboards import CommonKeyboard

router = Router(name=__name__)

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

class MessageDateFSM(StatesGroup):
    first = State()
    second = State()

@router.message(F.text.lower() == CalcDatetimeText.CALC_TEXT.lower())
async def command_timedelta_handler(msg: Message, state: FSMContext) -> None:
    if not await is_staff(msg.from_user.username):
        await msg.reply(f"Функция недоступна")
        return
    await state.set_state(MessageDateFSM.first)
    await msg.reply("Введите первую дату", reply_markup=CommonKeyboard().input_state().markup())


@router.message(MessageDateFSM.first)
async def command_timedelta_first_handler(msg: Message, state: FSMContext):
    text = msg.text or msg.caption
    if text.lower() == AdminText.CANCEL.lower():
        await msg.answer("Отмена операции", kb=CommonKeyboard().main_state().markup())
        return

    date_str = text.split()[0]
    await state.update_data(first=date_str)
    await state.set_state(MessageDateFSM.second)
    await msg.reply("Введите вторую дату", reply_markup=CommonKeyboard().input_state().markup())

@router.message(MessageDateFSM.second)
async def command_timedelta_second_handler(msg: Message, state: FSMContext):
    text = msg.text or msg.caption
    if text.lower() == AdminText.CANCEL.lower():
        await msg.answer("Отмена операции", kb=CommonKeyboard().main_state().markup())
        return

    date2_str = text.split()[0]
    date1_str = await state.get_value("first")
    delta_date, status = get_timedelta_urls(date1_str, date2_str)
    await state.clear()
    kb = CommonKeyboard().main_state()
    if delta_date:
        await msg.reply(f"Прошло {abs(delta_date.days)} дней", reply_markup=kb.markup())
    else:
        await msg.reply(status, reply_markup=kb.markup())

