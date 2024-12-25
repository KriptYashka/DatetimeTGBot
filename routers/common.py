from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from resourses.text import AdminText
from routers.keyboard.keyboards import CommonKeyboard

router = Router(name=__name__)

kb = CommonKeyboard()

@router.message(F.text.lower() == AdminText.BACK_TO_MAIN.lower())
async def command_main_menu_handler(msg: Message):
    kb.main_state()
    await msg.answer("Возвращение в главное меню", reply_markup=kb.markup())