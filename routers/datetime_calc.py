from datetime import datetime
from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils.markdown import hbold

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

router = Router(name=__name__)

kb = [
    [   # 1 row of buttons for Navigation calendar
        # where user can go to next/previous year/month
        KeyboardButton(text='Navigation Calendar'),
        KeyboardButton(text='Navigation Calendar w month'),
    ],
    [   # 2 row of buttons for Dialog calendar
        # where user selects year first, then month, then day
        KeyboardButton(text='Dialog Calendar'),
        KeyboardButton(text='Dialog Calendar w year'),
        KeyboardButton(text='Dialog Calendar w month'),
    ],
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Hello, {hbold(message.from_user.full_name)}! Pick a calendar", reply_markup=start_kb)

@router.message(F.text.lower() == 'navigation calendar')
async def nav_cal_handler(message: Message):
    await message.answer(
        "Выберите дату начала: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
    )

@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2000, 1, 1), datetime(2029, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )