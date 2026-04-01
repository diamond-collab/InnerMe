from aiogram.fsm.state import State, StatesGroup


class AddQuestionsState(StatesGroup):
    waiting_for_questions = State()
    waiting_for_reverse_questions = State()
