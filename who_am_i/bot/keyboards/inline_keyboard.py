from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from who_am_i.core.models import QuizORM, AnswerOptionORM


class QuizData(CallbackData, prefix='quiz'):
    slug: str


class AnswerData(CallbackData, prefix='answer'):
    attempt_id: int
    question_id: int
    option_id: int


class ProgressData(CallbackData, prefix='progress'):
    action: str
    attempt_id: int


def build_quizzes_keyboard(quizzes: list[QuizORM]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.adjust(1)

    for quiz in quizzes:
        builder.button(
            text=quiz.title,
            callback_data=QuizData(slug=quiz.slug),
        )

    return builder.as_markup()


def build_answers_keyboard(
    options: list[AnswerOptionORM],
    attempt_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for option in options:
        builder.button(
            text=option.label,
            callback_data=AnswerData(
                attempt_id=attempt_id,
                question_id=option.question_id,
                option_id=option.option_id,
            ),
        )

    builder.adjust(2, 2)

    return builder.as_markup()


def build_progress_keyboard(attempt_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Начать заново 🔄',
        callback_data=ProgressData(
            action='restart',
            attempt_id=attempt_id,
        ),
    )

    builder.button(
        text='Продолжить ▶️',
        callback_data=ProgressData(
            action='continue',
            attempt_id=attempt_id,
        ),
    )

    builder.adjust(1)

    return builder.as_markup()
