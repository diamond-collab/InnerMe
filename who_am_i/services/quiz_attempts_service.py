import random

from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAttemptORM
from who_am_i.repositories import quiz_attempts_repo


async def create_quiz_attempts(session: AsyncSession, quiz_id: int, user_id: int) -> QuizAttemptORM:
    seed = random.randint(1, 1_000_000)
    quiz_attempt = await quiz_attempts_repo.create_quiz_attempt(
        session=session,
        quiz_id=quiz_id,
        user_id=user_id,
        seed=seed,
    )
    return quiz_attempt


async def get_attempt_by_id(
    session: AsyncSession,
    attempt_id: int,
) -> QuizAttemptORM:
    attempt = await quiz_attempts_repo.get_attempt_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    return attempt


async def update_quiz_attempt(
    session: AsyncSession,
    attempt_id: int,
    result_score: int,
    result_percent: int,
) -> QuizAttemptORM:
    quiz_attempt = await quiz_attempts_repo.update_quiz_attempt(
        session=session,
        attempt_id=attempt_id,
        result_score=result_score,
        result_percent=result_percent,
    )
    return quiz_attempt


async def get_in_progress_attempt(
    session: AsyncSession,
    user_id: int,
    quiz_id: int,
) -> QuizAttemptORM:
    return await quiz_attempts_repo.get_in_progress_attempt(
        session=session,
        user_id=user_id,
        quiz_id=quiz_id,
    )


async def cancel_attempt(session: AsyncSession, attempt_id: int) -> None:
    return await quiz_attempts_repo.cancel_attempt(session=session, attempt_id=attempt_id)


async def finished_attempt(
    session: AsyncSession,
    attempt_id: int,
) -> None:
    return await quiz_attempts_repo.finished_attempt(
        session=session,
        attempt_id=attempt_id,
    )
