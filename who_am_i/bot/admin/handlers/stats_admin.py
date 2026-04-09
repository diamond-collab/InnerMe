from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import (
    StatsPageData,
    QuizStatsData,
    build_back_to_quiz_keyboard,
    BackToStatsPageData,
)
from who_am_i.bot.admin.views import render_quiz_list_stats
from who_am_i.services import quiz_service, stats_service
from who_am_i.utils import pluralize


router = Router()


@router.callback_query(StatsPageData.filter())
async def handle_pagination_stats(
    callback: CallbackQuery,
    callback_data: StatsPageData,
    session: AsyncSession,
):
    page = callback_data.page

    quizzes = await quiz_service.get_all_quizzes(session=session)
    await render_quiz_list_stats(callback=callback, quizzes=quizzes, session=session, page=page)


@router.callback_query(QuizStatsData.filter())
async def handle_quiz_stats_view(
    callback: CallbackQuery,
    callback_data: QuizStatsData,
    session: AsyncSession,
):
    quiz_id = callback_data.quiz_id
    quiz = await quiz_service.get_quiz_by_id(session=session, quiz_id=quiz_id)
    if not quiz:
        await callback.answer('Нет доступных тестов')
        return

    quiz_stats = await stats_service.get_quiz_stats(
        session=session,
        quiz_id=quiz_id,
    )
    if not quiz_stats:
        await callback.answer('Нет пройденных тестов')
        return

    ranges = await stats_service.get_quiz_result_ranges(
        session=session,
        quiz_id=quiz_id,
    )
    if ranges is None:
        await callback.answer('Еще ни один пользователь не проходил тест')

    lines = list()
    for stats in ranges:
        lines.append(f'{stats["min"]} - {stats["max"]}% -> {stats["count"]} чел')
    text = '\n'.join(lines)

    attempt_word = pluralize(quiz_stats.total_attempts, ('раз', 'раза', 'раз'))
    await callback.message.answer(
        f'📋 {quiz.title}\n\n'
        f'📊 Пройдено: {quiz_stats.total_attempts} {attempt_word}\n'
        f'👥 Уникальных пользоватлей: {quiz_stats.unique_users}\n'
        f'📈 Средний результат прохождений: {quiz_stats.avg_result}%\n\n'
        f'📊 Результаты прохождений\n\n'
        f'{text}',
        reply_markup=build_back_to_quiz_keyboard(callback_data.page),
    )


@router.callback_query(BackToStatsPageData.filter())
async def handle_back_to_stats_list(
    callback: CallbackQuery,
    callback_data: BackToStatsPageData,
    session: AsyncSession,
):
    quizzes = await quiz_service.get_all_quizzes(session=session)
    page = callback_data.page

    await render_quiz_list_stats(callback=callback, quizzes=quizzes, session=session, page=page)
