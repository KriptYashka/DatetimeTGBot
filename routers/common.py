from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from resourses.text import AdminText
from routers.admin.moderate_user import is_admin
from routers.keyboard.keyboards import CommonKeyboard

router = Router(name=__name__)

@router.message(F.text.lower() == AdminText.BACK_TO_MAIN.lower())
async def command_main_menu_handler(msg: Message):
    kb = CommonKeyboard()
    kb.is_admin = is_admin(msg.from_user.username)
    await msg.answer("Возвращение в главное меню", reply_markup=kb.main_state().markup())