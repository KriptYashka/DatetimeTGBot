from abc import ABC
from typing import Optional, Type

from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from resourses.phrase import AdminText


class BaseState(ABC):
    buttons: list[list[ReplyKeyboardBuilder]] = []

    @classmethod
    def set_keyboard(cls, inline_keyboard: ReplyKeyboardBuilder):
        for row in cls.buttons:
            inline_keyboard.row(*row)


class MainState(BaseState):
    buttons = [
        [
            KeyboardButton(text=AdminText.SEE_MODERATOR)
        ],
        [
            KeyboardButton(text=AdminText.ADD_MODERATOR),
            KeyboardButton(text=AdminText.DELETE_MODERATOR),
        ]
    ]

class InputState(BaseState):
    buttons = [
        [
            KeyboardButton(text=AdminText.CANCEL)
        ]
    ]

class BaseKeyboard:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()
        self.state = BaseState

    def set_state(self, state: Type[BaseState]):
        self.state = state
        self.state.set_keyboard(self.builder)

    def markup(self):
        return self.builder.as_markup()



class AdminKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()

    def main_state(self):
        self.set_state(MainState)

    def input_state(self):
        self.set_state(InputState)