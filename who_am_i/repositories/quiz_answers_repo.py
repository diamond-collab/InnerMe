from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAnswers


async def create_quiz_answer(
        session: AsyncSession,
        attempt_id: int,
        question_id: int,
        option_id: int,
        value: int,
) -> QuizAnswers:
    quiz_answer = QuizAnswers(
        attempt_id=attempt_id,
        question_id=question_id,
        option_id=option_id,
        value=value,
    )
    session.add(quiz_answer)
    await session.flush()
    return quiz_answer


async def get_quiz_answers_by_id(
        session: AsyncSession,
        attempt_id: int,
) -> list[QuizAnswers]:
    stmt = select(QuizAnswers).where(QuizAnswers.attempt_id == attempt_id)
    result = list((await session.scalars(stmt)).all())
    return result


async def get_answer_by_attempt_and_question(
        session: AsyncSession,
        attempt_id: int,
        question_id: int,
) -> QuizAnswers | None:
    stmt = select(QuizAnswers).where(
        QuizAnswers.attempt_id == attempt_id,
        QuizAnswers.question_id == question_id,
    )
    result = await session.scalar(stmt)
    return result
