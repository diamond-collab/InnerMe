from aiogram.fsm.state import State, StatesGroup


class AddQuizState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
