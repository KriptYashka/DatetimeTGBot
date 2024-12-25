from typing import Type

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from routers.keyboard.states import InputState, AdminMainState, BaseState, CommonMainState


class BaseKeyboard:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()
        self.state = BaseState

    def set_state(self, state: Type[BaseState]):
        self.state = state
        self.state.set_keyboard(self.builder)
        return self

    def input_state(self):
        return self.set_state(InputState)

    def markup(self):
        return self.builder.as_markup()

class CommonKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()

    def main_state(self):
        return self.set_state(CommonMainState)


class AdminKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()

    def main_state(self):
        return self.set_state(AdminMainState)
