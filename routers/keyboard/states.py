from abc import ABC

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from resourses.text import AdminText, CalcDatetimeText


class BaseState(ABC):
    buttons: list[list[ReplyKeyboardBuilder]] = []

    @classmethod
    def set_keyboard(cls, inline_keyboard: ReplyKeyboardBuilder):
        for row in cls.buttons:
            inline_keyboard.row(*row)


class InputState(BaseState):
    buttons = [
        [
            KeyboardButton(text=AdminText.CANCEL)
        ]
    ]

class CommonMainState(BaseState):
    buttons = [
    [
        KeyboardButton(text=CalcDatetimeText.CALC_CALENDAR),
    ],
    [
        KeyboardButton(text=CalcDatetimeText.CALC_TEXT),
    ],
]

class AdminMainState(BaseState):
    buttons = [
        [
            KeyboardButton(text=AdminText.SHOW_MODERATORS)
        ],
        [
            KeyboardButton(text=AdminText.ADD_MODERATOR),
            KeyboardButton(text=AdminText.DELETE_MODERATOR),
        ],
        [
            KeyboardButton(text=AdminText.BACK_TO_MAIN),
        ]
    ]
