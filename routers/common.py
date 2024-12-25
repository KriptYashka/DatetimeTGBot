from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from resourses.text import AdminText

router = Router(name=__name__)

@router.message(F.text.lower() == AdminText.BACK_TO_MAIN.lower())
async def command_main_menu_handler(msg: Message):
    kb = [
        [
            KeyboardButton(text='Подсчёт дней: Календарь'),
            KeyboardButton(text='Подсчёт дней: Текст с постов'),
        ]
    ]
    start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer("Возвращение в главное меню", reply_markup=start_kb)