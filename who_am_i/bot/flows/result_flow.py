import logging

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import quiz_answers_service, quiz_attempts_service

logger = logging.getLogger(__name__)


async def finish_quiz_attempt(
    callback: CallbackQuery,
    attempt_id: int,
    session: AsyncSession,
) -> None:
    quiz_answers = await quiz_answers_service.get_quiz_answers_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if not quiz_answers:
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось завершить тест: ответы не найдены. Попробуй пройти его заново.</b>'
        )
        return

    result_score = sum(answer.value for answer in quiz_answers)
    min_score = len(quiz_answers) * 1
    max_score = len(quiz_answers) * 4
    result_percent = (result_score - min_score) / (max_score - min_score) * 100
    result_percent = round(result_percent)

    quiz_attempt = await quiz_attempts_service.update_quiz_attempt(
        session=session,
        attempt_id=attempt_id,
        result_score=result_score,
        result_percent=result_percent,
    )
    if quiz_attempt is None:
        await callback.answer()
        await callback.message.answer(f'<b>Результат сейчас недоступен</b>')
        return

    logger.info('attempt_id: %s', quiz_attempt.attempt_id)
    logger.info('result_score: %s', quiz_attempt.result_score)
    logger.info('result_percent: %s', quiz_attempt.result_percent)

    await callback.answer()
    await callback.message.answer(f'<b>Твой результат {quiz_attempt.result_score}</b>')
