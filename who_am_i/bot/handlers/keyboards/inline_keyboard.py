from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from who_am_i.core.models import QuizORM


class QuizData(CallbackData, prefix='quiz'):
    slug: str


def build_quizzes_keyboard(quizzes: list[QuizORM]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.adjust(1)

    for quiz in quizzes:
        builder.button(
            text=quiz.title,
            callback_data=QuizData(slug=quiz.slug),
        )

    return builder.as_markup()
