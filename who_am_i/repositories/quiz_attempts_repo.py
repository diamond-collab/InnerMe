from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAttemptORM, Status


async def create_quiz_attempt(
    session: AsyncSession,
    quiz_id: int,
    user_id: int,
    seed: int,
) -> QuizAttemptORM:
    quiz_attempt = QuizAttemptORM(
        user_id=user_id,
        quiz_id=quiz_id,
        seed=seed,
    )
    session.add(quiz_attempt)
    await session.flush()
    return quiz_attempt


async def get_attempt_by_id(session: AsyncSession, attempt_id: int) -> QuizAttemptORM | None:
    stmt = select(QuizAttemptORM).where(QuizAttemptORM.attempt_id == attempt_id)
    result = await session.scalar(stmt)
    return result


async def update_quiz_attempt(
    session: AsyncSession,
    attempt_id: int,
    result_score: int,
    result_percent: int,
) -> QuizAttemptORM | None:
    attempt: QuizAttemptORM | None = await session.get(QuizAttemptORM, attempt_id)
    if attempt is None:
        return None

    attempt.status = Status.FINISHED
    attempt.result_score = result_score
    attempt.result_percent = result_percent
    attempt.finished_at = datetime.now(timezone.utc)

    await session.flush()
    return attempt


async def get_in_progress_attempt(
    session: AsyncSession,
    user_id: int,
    quiz_id: int,
) -> QuizAttemptORM | None:
    stmt = (
        select(QuizAttemptORM)
        .where(
            QuizAttemptORM.user_id == user_id,
            QuizAttemptORM.quiz_id == quiz_id,
            QuizAttemptORM.status == Status.IN_PROGRESS,
        )
        .order_by(QuizAttemptORM.started_at.desc())
    )
    result = await session.scalar(stmt)
    return result


async def cancel_attempt(
    session: AsyncSession,
    attempt_id: int,
) -> None:
    stmt = (
        update(QuizAttemptORM)
        .where(QuizAttemptORM.attempt_id == attempt_id)
        .values(
            status=Status.CANCELLED,
            finished_at=datetime.now(timezone.utc),
        )
    )
    await session.execute(stmt)


async def finished_attempt(
    session: AsyncSession,
    attempt_id: int,
) -> None:
    stmt = (
        update(QuizAttemptORM)
        .where(QuizAttemptORM.attempt_id == attempt_id)
        .values(
            status=Status.FINISHED,
            finished_at=datetime.now(timezone.utc),
        )
    )
    await session.execute(stmt)
