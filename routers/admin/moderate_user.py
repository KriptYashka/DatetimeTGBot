import os
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram import Router, F
from aiogram.filters import Command, CommandObject

from models import UserOrm
from repositories import UserRepository
from resourses.text import AdminText
from routers.keyboard.keyboards import AdminKeyboard, CommonKeyboard
from routers.keyboard.states import BaseState

router = Router(name=__name__)

kb = AdminKeyboard()

async def is_staff(tg_id: str):
    user = await UserRepository.get_user_by_tg_id(tg_id.lower())
    if user is None:
        return None
    return user.is_staff

async def is_admin(tg_id: str):
    user = await UserRepository.get_user_by_tg_id(tg_id.lower())
    if user is None:
        return None
    return user.is_admin

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

@router.message(Command("admin_make"))
async def command_admin_panel_handler(msg: Message, command: CommandObject):
    tg_id = msg.from_user.username.lower()
    if await is_admin(tg_id):
        await msg.answer("Вы уже администратор", reply_markup=kb.main_state().markup())
        return
    if not command.args:
        return await msg.answer("Требуется токен авторизации после команды /admin_make")
    if command.args.strip() == os.getenv("TOKEN"):
        data = {
            "tg_id": tg_id,
            "datetime_register": datetime.now(),
            "is_staff": True,
            "is_admin": True
        }
        user = UserOrm(**data)
        await UserRepository.create_user(user)
        await msg.answer("Вы стали администратором", reply_markup=kb.main_state().markup())
    else:
        await msg.answer("Неверно введённые данные. Данный инцидент будет зафиксирован.", reply_markup=CommonKeyboard().main_state().markup())
    await msg.delete()

@router.message(Command("admin"))
async def command_admin_panel_handler(msg: Message):
    if not await is_admin(msg.from_user.username):
        await msg.reply(f"Функция недоступна")
        return
    await msg.answer("Активирована панель администратора", reply_markup=kb.main_state().markup())

class ModeratorFSM(StatesGroup):
    select_add = State()
    select_delete = State()

@router.message(F.text.lower() == AdminText.ADD_MODERATOR.lower())
async def command_select_moderator_handler(msg: Message, state: FSMContext):
    if not await is_admin(msg.from_user.username.lower()):
        await msg.reply(f"Функция недоступна")
        return
    await state.set_state(ModeratorFSM.select_add)
    await msg.reply(AdminText.ADD_MODERATOR_SELECT, reply_markup=kb.input_state().markup())

@router.message(ModeratorFSM.select_add)
async def command_add_moderator_handler(msg: Message, state: FSMContext):
    await state.clear()
    if msg.text.lower() == AdminText.CANCEL.lower():
        await msg.answer("Отмена операции")
        await command_admin_panel_handler(msg)
        return

    tg_id = msg.text.replace("@", "").strip().lower()

    data = {
        "tg_id": tg_id,
        "datetime_register": datetime.now(),
        "is_staff": True
    }
    user = UserOrm(**data)
    await UserRepository.create_user(user)

    await msg.reply(AdminText.ADD_MODERATOR_SUCCESS.format(tg_id), reply_markup=kb.main_state().markup())

@router.message(F.text.lower() == AdminText.SHOW_MODERATORS.lower())
async def command_show_moderators_handler(msg: Message):
    if not await is_admin(msg.from_user.username):
        await msg.reply(f"Функция недоступна")
        return

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
    if not await is_admin(msg.from_user.username.lower()):
        await msg.reply(f"Функция недоступна")
        return

    await state.set_state(ModeratorFSM.select_delete)
    await msg.reply(AdminText.DELETE_MODERATOR_SELECT, reply_markup=kb.markup())

@router.message(ModeratorFSM.select_delete)
async def command_delete_moderator_handler(msg: Message, state: FSMContext):
    await state.clear()
    if msg.text == AdminText.CANCEL:
        await msg.answer("Отмена операции")
        await command_admin_panel_handler(msg)
        return

    tg_id = msg.text.replace("@", "").strip()
    if await UserRepository.get_user_by_tg_id(tg_id) is None:
        await msg.reply(
            AdminText.DELETE_MODERATOR_DENIED.format(tg_id), reply_markup=kb.main_state().markup()
        )
        return
    await UserRepository.delete_user_by_tg_id(tg_id)

    await msg.reply(
        AdminText.DELETE_MODERATOR_SUCCESS.format(tg_id), reply_markup=kb.main_state().markup()
    )