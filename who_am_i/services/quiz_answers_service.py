from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAnswers
from who_am_i.repositories import quiz_answers_repo


async def create_quiz_answer(
    session: AsyncSession,
    attempt_id: int,
    question_id: int,
    option_id: int,
    value: int,
) -> QuizAnswers:
    quiz_answer = await quiz_answers_repo.create_quiz_answer(
        session=session,
        attempt_id=attempt_id,
        question_id=question_id,
        option_id=option_id,
        value=value,
    )
    return quiz_answer


async def get_quiz_answers_by_id(
    session: AsyncSession,
    attempt_id: int,
) -> list[QuizAnswers]:
    quiz_answers = await quiz_answers_repo.get_quiz_answers_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    return quiz_answers


async def get_answer_by_attempt_and_question(
    session: AsyncSession,
    attempt_id: int,
    question_id: int,
) -> QuizAnswers | None:
    return await quiz_answers_repo.get_answer_by_attempt_and_question(
        session=session,
        attempt_id=attempt_id,
        question_id=question_id,
    )
