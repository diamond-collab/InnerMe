from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import (
    StatsPageData,
    QuizStatsData,
    build_back_to_quiz_keyboard,
    main_admin_menu_keyboard,
)
from who_am_i.bot.admin.views import render_quiz_list_stats
from who_am_i.bot.admin.views.stats_quiz_view import render_popular_quizzes_stats
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
    if callback_data.mode == 'default':
        quizzes = await quiz_service.get_all_quizzes(session=session)
        await render_quiz_list_stats(
            callback=callback,
            items=quizzes,
            session=session,
            page=page,
            mode=callback_data.mode,
        )
    else:
        popular_quizzes = await stats_service.get_popular_quiz_stats(
            session=session,
        )
        await render_popular_quizzes_stats(
            callback=callback,
            items=popular_quizzes,
            page=callback_data.page,
            mode=callback_data.mode,
        )


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

    if not ranges:
        await callback.answer()
        await callback.message.answer(
            'По этому тесту пока нет статистики по диапазонам результатов.'
        )
        return

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
        reply_markup=build_back_to_quiz_keyboard(callback_data.page, callback_data.mode),
    )


@router.callback_query(StatsPageData.filter())
async def handle_back_to_stats_list(
    callback: CallbackQuery,
    callback_data: StatsPageData,
    session: AsyncSession,
):
    quizzes = await quiz_service.get_all_quizzes(session=session)
    page = callback_data.page

    await render_quiz_list_stats(
        callback=callback,
        items=quizzes,
        session=session,
        page=page,
        mode=callback_data.mode,
    )


@router.callback_query(lambda c: c.data == 'admin_menu')
async def handle_back_to_menu(
    callback: CallbackQuery,
):
    await callback.message.answer(
        'Админ меню',
        reply_markup=main_admin_menu_keyboard(),
    )
    await callback.answer()
