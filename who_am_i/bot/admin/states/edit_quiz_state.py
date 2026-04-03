from aiogram.fsm.state import StatesGroup, State


class EditState(StatesGroup):
    waiting_for_new_title = State()
    waiting_for_new_description = State()
