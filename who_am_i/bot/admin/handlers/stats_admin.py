from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import StatsPageData, QuizStatsData
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

    total_attempts = await stats_service.get_finished_quiz(
        session=session,
        quiz_id=quiz.quiz_id,  # type: ignore
    )
    unique_users_count = await stats_service.get_finished_attempts_users(
        session=session,
        quiz_id=quiz_id,
    )
    attempt_scores = await stats_service.get_scores_finished_attempts(
        session=session,
        quiz_id=quiz_id,
    )
    if not attempt_scores:
        await callback.answer('Нет пройденных тестов')
        return

    total_score = sum(i.result_score for i in attempt_scores)
    avg_result = total_score / len(attempt_scores)

    attempt_word = pluralize(total_attempts, ('раз', 'раза', 'раз'))
    await callback.message.answer(
        f'📋 {quiz.title}\n\n'
        f'📊 Пройдено: {total_attempts} {attempt_word}\n'
        f'👥 Уникальных пользоватлей: {unique_users_count}\n'
        f'📈 Средний результат прохождений: {int(avg_result)}%'
    )
