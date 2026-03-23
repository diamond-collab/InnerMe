import logging

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import quiz_answers_service, quiz_attempts_service, result_service
from who_am_i.utils import pluralize

logger = logging.getLogger(__name__)


async def finish_quiz_attempt(
    callback: CallbackQuery,
    attempt_id: int,
    session: AsyncSession,
) -> None:
    await callback.answer()

    quiz_answers = await quiz_answers_service.get_quiz_answers_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if not quiz_answers:
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
        await callback.message.answer(f'<b>Результат сейчас недоступен</b>')
        return

    result = await result_service.get_result(
        session=session,
        quiz_id=quiz_attempt.quiz_id,
        result_percent=result_percent,
    )
    if result is None:
        await callback.message.answer(
            f'<b>📊 Результат теста</b>\n\n'
            f'<b>Твой результат: {result_score} '
            f'{pluralize(result_score, ("балл", "балла", "баллов"))} '
            f'({result_percent}%)</b>\n\n'
            f'<i>Пока для этого результата нет подробного описания.\n</i>'
            f'<i>Попробуй пройти тест позже — мы скоро добавим интерпретацию.</i>'
        )
        return

    logger.info('attempt_id: %s', quiz_attempt.attempt_id)
    logger.info('result_score: %s', quiz_attempt.result_score)
    logger.info('result_percent: %s', quiz_attempt.result_percent)

    result_text, result_range = result

    advice_text = ''
    if result_text.advice:
        advice_text = f'\n\n<b>💡 Рекомендация:</b>\n\n<i>{result_text.advice}</i>'

    await callback.message.answer(
        f'<b>📊 Результат теста</b>\n\n'
        f'<b>Твой результат: {result_score} '
        f'{pluralize(result_score, ("балл", "балла", "баллов"))} '
        f'({result_percent}%)</b>\n\n'
        f'<b>Уровень: {result_range.title}</b>\n\n'
        f'<b>Описание:</b>\n\n'
        f'<i>{result_text.description}</i>{advice_text}'
    )
