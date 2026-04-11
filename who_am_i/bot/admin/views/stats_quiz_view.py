from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.utils import pagination_of_buttons
from who_am_i.bot.admin.keyboards import build_stats_admin_keyboard
from who_am_i.bot.admin.utils import build_stats_text, build_popular_stats_text
from who_am_i.services import stats_service


async def render_quiz_list_stats(
    callback: CallbackQuery,
    items: list,
    session: AsyncSession,
    page: int,
    mode: str,
) -> None:
    await callback.answer()

    has_prev, has_next, page_quizzes = await pagination_of_buttons(
        items=items,
        page=page,
    )

    kb = build_stats_admin_keyboard(
        quizzes=page_quizzes,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
        mode=mode,
    )
    stats = await stats_service.get_common_stats(
        session=session,
    )

    text = build_stats_text(
        stats=stats,
    )
    await callback.message.edit_text(text, reply_markup=kb)


async def render_popular_quizzes_stats(
    callback: CallbackQuery,
    items: list,
    page: int,
    mode: str,
) -> None:
    await callback.answer()
    has_prev, has_next, page_quizzes = await pagination_of_buttons(
        items=items,
        page=page,
    )
    kb = build_stats_admin_keyboard(
        quizzes=page_quizzes,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
        mode=mode,
    )
    text = build_popular_stats_text(items=page_quizzes)

    await callback.message.edit_text(text, reply_markup=kb)
