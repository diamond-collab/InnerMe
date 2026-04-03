from aiogram.fsm.state import State, StatesGroup


class EditQuestionState(StatesGroup):
    waiting_for_new_text_question = State()
