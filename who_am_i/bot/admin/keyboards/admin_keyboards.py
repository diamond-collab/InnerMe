from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData

from who_am_i.core.models import QuizORM


class QuizData(CallbackData, prefix='quiz'):
    quiz_id: int
    page: int


class AddQuizData(CallbackData, prefix='add_quiz'):
    pass


class TestsPageData(CallbackData, prefix='tests_page'):
    page: int


class EditQuizData(CallbackData, prefix='edit_quiz'):
    quiz_id: int
    page: int
    action: str


class ReverseQuestionsData(CallbackData, prefix='reverse_questions'):
    quiz_id: int
    page: int
    action: str


def main_admin_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='📋 Тесты'),
                KeyboardButton(text='📊 Статистика'),
            ],
            [
                KeyboardButton(text='🔙 Назад'),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def inline_build_tests_keyboard(
    quizzes: list[QuizORM],
    page: int,
    has_prev: bool,
    has_next: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for quiz in quizzes:
        builder.button(
            text=quiz.title,
            callback_data=QuizData(
                quiz_id=quiz.quiz_id,
                page=page,
            ).pack(),
        )
    builder.adjust(2)

    nav_buttons = list()
    if has_prev:
        nav_buttons.append(
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=TestsPageData(page=page - 1).pack(),
            ),
        )

    if has_next:
        nav_buttons.append(
            InlineKeyboardButton(
                text='🔜 Вперед',
                callback_data=TestsPageData(page=page + 1).pack(),
            ),
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.button(
        text='➕ Добавить тест',
        callback_data=AddQuizData().pack(),
    )
    builder.button(text='🔚 В меню', callback_data='admin_menu')

    return builder.as_markup()


def build_quiz_actions_keyboard(quiz: QuizORM, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='📝 Добавить вопрос',
        callback_data=EditQuizData(quiz_id=quiz.quiz_id, page=page, action='add_question'),
    )
    builder.button(
        text='❓Вопросы',
        callback_data=EditQuizData(quiz_id=quiz.quiz_id, page=page, action='questions'),
    )
    builder.button(
        text='✏️ Редактировать',
        callback_data=EditQuizData(quiz_id=quiz.quiz_id, page=page, action='edit'),
    )

    builder.button(
        text='🔁 Вкл/Выкл',
        callback_data=EditQuizData(quiz_id=quiz.quiz_id, page=page, action='toggle'),
    )
    builder.button(
        text='🔙 К списку',
        callback_data=EditQuizData(
            quiz_id=quiz.quiz_id,
            page=page,
            action='back',
        ),
    )

    builder.adjust(2, 2)
    return builder.as_markup()


def inline_back_to_quiz_keyboard(quiz_id: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='🔙 К тесту',
        callback_data=QuizData(
            quiz_id=quiz_id,
            page=page,
        ).pack(),
    )
    return builder.as_markup()


def inline_edit_quiz_keyboard(quiz_id: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Название теста',
        callback_data=EditQuizData(
            quiz_id=quiz_id,
            page=page,
            action='edit_title',
        ).pack(),
    )
    builder.button(
        text='Описание',
        callback_data=EditQuizData(
            quiz_id=quiz_id,
            page=page,
            action='edit_description',
        ).pack(),
    )

    builder.button(
        text='🔙 К тесту',
        callback_data=QuizData(
            quiz_id=quiz_id,
            page=page,
        ).pack(),
    )
    builder.adjust(2, 2)
    return builder.as_markup()


def inline_reverse_questions_keyboard(
    quiz_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='✅ Да',
        callback_data=ReverseQuestionsData(
            quiz_id=quiz_id,
            page=page,
            action='yes',
        ),
    )
    builder.button(
        text='❌ Нет',
        callback_data=ReverseQuestionsData(
            quiz_id=quiz_id,
            page=page,
            action='no',
        ),
    )
    builder.adjust(2)
    return builder.as_markup()
