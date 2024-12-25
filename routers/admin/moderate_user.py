from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram import Router, F
from aiogram.filters import Command

from models import UserOrm
from repositories import UserRepository
from resourses.text import AdminText
from routers.keyboard.keyboards import AdminKeyboard

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

@router.message(Command("admin"))
async def command_admin_panel_handler(msg: Message):
    kb = AdminKeyboard().main_state()
    await msg.answer("Активирована панель администратора", reply_markup=kb.markup())

class ModeratorFSM(StatesGroup):
    select_add = State()
    select_delete = State()

@router.message(F.text.lower() == AdminText.ADD_MODERATOR.lower())
async def command_select_moderator_handler(msg: Message, state: FSMContext):
    await state.set_state(ModeratorFSM.select_add)
    kb = AdminKeyboard().input_state()
    await msg.reply(AdminText.ADD_MODERATOR_SELECT, reply_markup=kb.markup())

@router.message(ModeratorFSM.select_add)
async def command_add_moderator_handler(msg: Message, state: FSMContext):
    await state.clear()
    if msg.text == AdminText.CANCEL:
        await msg.answer("Отмена операции")
        await command_admin_panel_handler(msg)
        return
    tg_id = msg.text.replace("@", "").strip()

    data = {
        "tg_id": tg_id,
        "datetime_register": datetime.now(),
        "is_staff": True
    }
    user = UserOrm(**data)
    await UserRepository.create_user(user)

    await msg.reply(AdminText.ADD_MODERATOR_SUCCESS.format(tg_id))

@router.message(F.text.lower() == AdminText.SHOW_MODERATORS.lower())
async def command_show_moderators_handler(msg: Message):
    users = await UserRepository.get_staff_users()
    data_users = []
    for index, user in enumerate(users):
        dt: datetime = user.datetime_register
        data = f"{index + 1}. {dt.strftime('%d/%m/%Y')} - @{user.tg_id}"
        data_users.append(data)
    text = "\n".join(data_users)
    await msg.answer(text)

@router.message(F.text.lower() == AdminText.DELETE_MODERATOR.lower())
async def command_delete_select_moderator_handler(msg: Message, state: FSMContext):
    await state.set_state(ModeratorFSM.select_delete)
    kb = AdminKeyboard().input_state()
    await msg.reply(AdminText.DELETE_MODERATOR_SELECT, reply_markup=kb.markup())

@router.message(ModeratorFSM.select_delete)
async def command_delete_moderator_handler(msg: Message, state: FSMContext):
    await state.clear()
    if msg.text == AdminText.CANCEL:
        await msg.answer("Отмена операции")
        await command_admin_panel_handler(msg)
        return

    tg_id = msg.text.replace("@", "").strip()
    print("ID:" ,tg_id)
    await UserRepository.delete_user_by_tg_id(tg_id)

    await msg.reply(
        AdminText.DELETE_MODERATOR_SUCCESS.format(tg_id), reply_markup=AdminKeyboard().main_state().markup()
    )