import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import user_service, quiz_attempts_service
from who_am_i.utils import pluralize

logger = logging.getLogger(__name__)

router = Router()


async def render_stats(
    message: Message,
    session: AsyncSession,
):
    tg_id = message.from_user.id
    logger.info('telegram_id: %s', tg_id)
    user = await user_service.get_current_user(
        session=session,
        telegram_id=tg_id,
    )
    if user is None:
        await message.answer('какое то сообщение')
        return

    attempts_with_quizzes = (
        await quiz_attempts_service.get_finished_attempts_with_quizzes_by_user_id(
            session=session,
            user_id=user.user_id,
        )
    )
    if not attempts_with_quizzes:
        await message.answer(
            f'<b>У тебя еще нет пройденных тестов</b>\n\n<i>Можешь выбрать тест, в разделе "Тесты" либо просто введи команды /test</i>'
        )
        return

    counter_attempts = len(attempts_with_quizzes)
    stats_by_quiz = dict()
    unique_quiz_ids = set()
    for attempt, quiz in attempts_with_quizzes:
        if quiz is None:
            continue

        if quiz.quiz_id not in stats_by_quiz:
            stats_by_quiz[quiz.quiz_id] = {
                'title': quiz.title,
                'count': 1,
                'best_percent': attempt.result_percent,
                'best_score': attempt.result_score,
                'last_percent': attempt.result_percent,
                'last_score': attempt.result_score,
                'last_finished_at': attempt.finished_at,
            }
        else:
            stats_by_quiz[quiz.quiz_id]['count'] += 1
            if attempt.result_percent > stats_by_quiz[quiz.quiz_id]['best_percent']:
                stats_by_quiz[quiz.quiz_id]['best_percent'] = attempt.result_percent
                stats_by_quiz[quiz.quiz_id]['best_score'] = attempt.result_score
            if attempt.finished_at > stats_by_quiz[quiz.quiz_id]['last_finished_at']:
                stats_by_quiz[quiz.quiz_id]['last_finished_at'] = attempt.finished_at
                stats_by_quiz[quiz.quiz_id]['last_percent'] = attempt.result_percent
                stats_by_quiz[quiz.quiz_id]['last_score'] = attempt.result_score

        unique_quiz_ids.add(quiz.quiz_id)

    unique_quizzes_count = len(unique_quiz_ids)
    messages = list()
    for stat in sorted(stats_by_quiz.values(), key=lambda x: x['best_percent'], reverse=True):
        msg = (
            f'• {stat["title"]} - {stat["count"]} {pluralize(stat["count"], ("попытка", "попытки", "попыток"))}\n'
            f'  👍 Лучший результат: {stat["best_percent"]}% ({stat["best_score"]} '
            f'{pluralize(stat["best_score"], ("балл", "балла", "баллов"))})\n'
            f'  📆 Последний результат: {stat["last_percent"]}% ({stat["last_score"]} '
            f'{pluralize(stat["last_score"], ("балл", "балла", "баллов"))})\n\n'
        )
        messages.append(msg)

    text = (
        f'📊 <b>Твоя статистика</b>\n\n'
        f'Пройдено разных тестов - {unique_quizzes_count}\n'
        f'Всего попыток: {counter_attempts}\n\n'
        f'<b>Результаты:</b>\n'
        f'{"".join(messages)}'
    )
    await message.answer(text)
