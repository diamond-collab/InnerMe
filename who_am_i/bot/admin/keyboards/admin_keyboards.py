from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData

from who_am_i.core.models import QuizORM, QuizQuestionORM


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


class QuestionData(CallbackData, prefix='question'):
    question_id: int
    quiz_id: int
    page: int


class AddQuestionData(CallbackData, prefix='add_question'):
    quiz_id: int
    page: int


class QuestionActionData(CallbackData, prefix='question_action'):
    question_id: int
    quiz_id: int
    page: int
    action: str


class QuizStatsData(CallbackData, prefix='quiz_stats'):
    quiz_id: int
    page: int


class StatsPageData(CallbackData, prefix='stats_page'):
    page: int
    mode: str  # 'default' | 'popular'


class BackToStatsPageData(CallbackData, prefix='back_to_quiz_stats'):
    page: int


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


def inline_questions_keyboard(
    questions: list[QuizQuestionORM],
    quiz_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for question in questions:
        builder.button(
            text=f'{question.order}. {question.text}',
            callback_data=QuestionData(
                question_id=question.question_id,
                quiz_id=quiz_id,
                page=page,
            ).pack(),
        )
    builder.adjust(1)

    buttons = list()
    buttons.append(
        InlineKeyboardButton(
            text='➕ Добавить вопрос',
            callback_data=EditQuizData(
                quiz_id=quiz_id,
                page=page,
                action='add_question',
            ).pack(),
        )
    )
    buttons.append(
        InlineKeyboardButton(
            text='🔙 К тесту',
            callback_data=QuizData(
                quiz_id=quiz_id,
                page=page,
            ).pack(),
        )
    )
    builder.row(*buttons)

    return builder.as_markup()


def build_question_actions_keyboard(
    question_id: int,
    quiz_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='✏️ Изменить текст',
        callback_data=QuestionActionData(
            question_id=question_id,
            quiz_id=quiz_id,
            page=page,
            action='edit_question',
        ).pack(),
    )
    builder.button(
        text='🔁 Сменить reverse',
        callback_data=QuestionActionData(
            question_id=question_id,
            quiz_id=quiz_id,
            page=page,
            action='edit_reverse',
        ).pack(),
    )
    builder.button(
        text='🔄 Вкл/Выкл',
        callback_data=QuestionActionData(
            question_id=question_id,
            quiz_id=quiz_id,
            page=page,
            action='edit_activ',
        ).pack(),
    )
    builder.button(
        text='🔙 К вопросам',
        callback_data=QuestionActionData(
            question_id=question_id,
            quiz_id=quiz_id,
            page=page,
            action='back_to_question',
        ),
    )

    builder.adjust(2, 2)
    return builder.as_markup()


def build_stats_admin_keyboard(
    quizzes: list[QuizORM],
    page: int,
    has_next: bool,
    has_prev: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for quiz in quizzes:
        builder.button(
            text=quiz.title,
            callback_data=QuizStatsData(
                quiz_id=quiz.quiz_id,
                page=page,
            ).pack(),
        )
    builder.adjust(1)

    nav_buttons = list()
    if has_next:
        nav_buttons.append(
            InlineKeyboardButton(
                text='🔜 Вперед',
                callback_data=StatsPageData(page=page + 1, mode='default').pack(),
            )
        )
    if has_prev:
        nav_buttons.append(
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=StatsPageData(page=page - 1, mode='default').pack(),
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(
            text='🔥 Популярные тесты',
            callback_data=StatsPageData(page=0, mode='popular').pack(),
        ),
        InlineKeyboardButton(
            text='🔚 В меню',
            callback_data='admin_menu',
        ),
    )
    return builder.as_markup()


def build_back_to_quiz_keyboard(page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Назад',
        callback_data=BackToStatsPageData(
            page=page,
        ),
    )
    return builder.as_markup()
