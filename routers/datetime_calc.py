import logging
from datetime import datetime, timedelta
from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InputFile, URLInputFile
from aiogram.utils.markdown import hbold

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback
from routers.admin.moderate_user import is_staff

router = Router(name=__name__)

class Form(StatesGroup):
    start_dt = State()
    end_dt = State()

kb = [
    [
        KeyboardButton(text='Подсчёт дней в промежутке'),
    ],
    [
        KeyboardButton(text='В разработке'),
    ],
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Приветствую, {hbold(message.from_user.full_name)}! Выбери одну из команд", reply_markup=start_kb)

@router.message(F.text.lower() == 'подсчёт дней в промежутке')
async def nav_cal_handler(message: Message, state: FSMContext):
    if not await is_staff(message.from_user.username):
        await message.reply(f"Функция недоступна")
        return
    await state.set_state(Form.start_dt)
    loc = await get_user_locale(message.from_user)
    await state.update_data(loc=loc)
    await message.answer(
        "Выберите первую дату: ",
        reply_markup=await SimpleCalendar(locale=loc).start_calendar()
    )

@router.callback_query(SimpleCalendarCallback.filter(), Form.start_dt)
async def process_start_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    loc = data["loc"]
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(
        datetime(2000, 1, 1),
        datetime(2029, 12, 31)
    )
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected and selected != "Cancel":
        await state.set_state(Form.end_dt)
        await state.update_data(dt=date)
        await callback_query.message.answer(
            f'Начало: {date.strftime("%d/%m/%Y")}'
        )
        await callback_query.message.answer(
            "Выберите вторую дату: ",
            reply_markup=await SimpleCalendar(locale=loc).start_calendar()
        )
        await callback_query.message.delete()
    elif selected == "Cancel":
        await callback_query.message.answer(
            f'Отмена операции.'
        )
        await callback_query.message.delete()
        await state.clear()

@router.callback_query(SimpleCalendarCallback.filter(), Form.end_dt)
async def process_end_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    data = await state.get_data()
    loc = data["loc"]
    calendar = SimpleCalendar(
        locale=loc, show_alerts=True
    )
    calendar.set_dates_range(
        datetime(2000, 1, 1),
        datetime(2029, 12, 31)
    )
    selected, end_date = await calendar.process_selection(callback_query, callback_data)
    if selected and selected != "Cancel":
        start_dt = data["dt"]
        diff_dt: timedelta = end_date - start_dt
        days = diff_dt.days

        text = f'От: {start_dt.strftime("%d/%m/%Y")}\nДо: {end_date.strftime("%d/%m/%Y")}\n📆 Количество дней между выбранными датами: {days} \n\n'


        await callback_query.message.answer(
            f'Конец: {end_date.strftime("%d/%m/%Y")}'
        )
        await callback_query.message.delete()
        photo = URLInputFile("https://freeimghost.net/images/2024/12/16/icon.jpg")
        await callback_query.message.answer_photo(photo=photo, caption=text, reply_markup=start_kb, show_caption_above_media=True)

        await state.clear()
    elif selected == "Cancel":
        await callback_query.message.answer(
            f'Отмена операции.'
        )
        await callback_query.message.delete()
        await state.clear()
