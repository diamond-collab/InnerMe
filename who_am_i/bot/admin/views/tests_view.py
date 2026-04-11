from aiogram.types import CallbackQuery

from who_am_i.core.models import QuizORM
from who_am_i.bot.admin.utils import pagination_of_buttons
from who_am_i.bot.admin.keyboards import inline_build_tests_keyboard


async def render_tests_list(
    callback: CallbackQuery,
    quizzes: list[QuizORM],
    page: int,
) -> None:
    has_prev, has_next, page_quizzes = await pagination_of_buttons(
        items=quizzes,
        page=page,
    )
    kb = inline_build_tests_keyboard(
        quizzes=page_quizzes,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
    )
    page_size = 5
    show_count = min((page + 1) * page_size, len(quizzes))

    await callback.message.edit_text(
        '<b>📋 Управление тестами\n\n'
        'Выбери тест из списка ниже.</b>\n'
        f'<i>Показано тестов: {show_count} из {len(quizzes)}</i>',
        reply_markup=kb,
    )
