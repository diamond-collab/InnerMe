from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    input_username = State()
    input_age = State()
