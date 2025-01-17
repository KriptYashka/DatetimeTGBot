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

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from resourses.text import CalcDatetimeText, CalcDatetimeText
from routers.admin.moderate_user import is_staff, is_admin
from routers.keyboard.keyboards import CommonKeyboard

router = Router(name=__name__)

class Form(StatesGroup):
    start_dt = State()
    end_dt = State()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = CommonKeyboard()
    kb.is_admin = await is_admin(message.from_user.username)
    text = f"Приветствую, {hbold(message.from_user.full_name)}! Выбери одну из команд"
    await message.reply(text, reply_markup=kb.main_state().markup())

@router.message(F.text.lower() == CalcDatetimeText.CALC_CALENDAR.lower())
async def nav_cal_handler(message: Message, state: FSMContext):
    if not await is_staff(message.from_user.username.lower()):
        await message.reply(f"Функция недоступна")
        return

    await state.set_state(Form.start_dt)
    await message.answer(
        "Выберите первую дату: ",
        reply_markup=await SimpleCalendar().start_calendar()
    )

@router.callback_query(SimpleCalendarCallback.filter(), Form.start_dt)
async def process_start_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(show_alerts=True)
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
            "Выберите вторую дату:",
            reply_markup=await SimpleCalendar().start_calendar()
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
    kb = CommonKeyboard()
    kb.is_admin = is_admin(callback_query.from_user.username)
    data = await state.get_data()
    calendar = SimpleCalendar()
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
        await callback_query.message.answer_photo(
            photo=photo, caption=text, reply_markup=kb.main_state().markup(), show_caption_above_media=True
        )

        await state.clear()
    elif selected == "Cancel":
        await callback_query.message.answer(
            f'Отмена операции.'
        )
        await callback_query.message.delete()
        await state.clear()

@router.message(Form.end_dt)
async def process_end_calendar_delta_days(msg: Message, state: FSMContext):
    kb = CommonKeyboard()
    kb.is_admin = await is_admin(msg.from_user.username)
    text = msg.text
    try:
        days = int(text)
    except TypeError:
        await msg.reply("Неверный формат ввода, попробуйте снова.")
        return

    date1 = await state.get_value("dt")
    date2 = date1 + timedelta(days)

    if days >= 0:
        text = f'📆Через {days} дня/дней от \n\n{date1.strftime("%d.%m.%Y")}\n\n будет \n\n{date2.strftime("%d.%m.%Y")}'
    else:
        text = f'📆{days * -1} дня/дней назад от \n\n{date1.strftime("%d.%m.%Y")}\n\n было \n\n{date2.strftime("%d.%m.%Y")}'
    photo = URLInputFile("https://freeimghost.net/images/2024/12/16/icon.jpg")
    await msg.answer_photo(
        photo=photo, caption=text, reply_markup=kb.main_state().markup(), show_caption_above_media=True
    )
    await state.clear()
