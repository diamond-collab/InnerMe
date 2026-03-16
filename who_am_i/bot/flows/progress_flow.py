from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAttemptORM
from who_am_i.services import quiz_attempts_service
from who_am_i.bot.flows.result_flow import finish_quiz_attempt
from who_am_i.bot.flows.question_flow import send_quiz_question
from who_am_i.services import quiz_questions_service


async def get_attempt_or_notify(
    callback: CallbackQuery,
    attempt_id: int,
    session: AsyncSession,
) -> QuizAttemptORM | None:
    attempt = await quiz_attempts_service.get_attempt_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if attempt is None:
        await callback.answer()
        await callback.message.answer(
            f'<b>Похоже, эта попытка теста уже завершена. Выбери тест заново.</b>'
        )
        return None

    return attempt


async def show_next_question_or_finish(
    callback: CallbackQuery,
    attempt: QuizAttemptORM,
    next_order: int,
    session: AsyncSession,
) -> None:
    next_question = await quiz_questions_service.get_question_by_id_and_order(
        session=session,
        quiz_id=attempt.quiz_id,
        order=next_order,
    )

    if next_question is None:
        await finish_quiz_attempt(
            callback=callback,
            attempt_id=attempt.attempt_id,
            session=session,
        )
        return

    await send_quiz_question(
        session=session,
        question=next_question,
        attempt_id=attempt.attempt_id,
        callback=callback,
    )
