from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.utils import pagination_of_buttons
from who_am_i.bot.admin.keyboards import build_stats_admin_keyboard
from who_am_i.bot.admin.utils import build_stats_text
from who_am_i.services import stats_service
from who_am_i.core.models import QuizORM


async def render_quiz_list_stats(
    callback: CallbackQuery,
    quizzes: list[QuizORM],
    session: AsyncSession,
    page: int,
) -> None:
    await callback.answer()

    has_prev, has_next, page_quizzes = await pagination_of_buttons(
        quizzes=quizzes,
        page=page,
    )

    kb = build_stats_admin_keyboard(
        quizzes=page_quizzes,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
    )
    stats = await stats_service.get_common_stats(
        session=session,
    )

    text = build_stats_text(
        stats=stats,
    )
    await callback.message.edit_text(text, reply_markup=kb)
