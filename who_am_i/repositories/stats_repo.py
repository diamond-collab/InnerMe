from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import UserORM, QuizORM, QuizAttemptORM, Status


async def get_all_users(session: AsyncSession) -> int:
    stmt = select(func.count(UserORM.user_id))
    count_users = await session.scalar(stmt)
    return count_users


async def get_all_finished_quizzes(session: AsyncSession) -> int:
    stmt = select(func.count(QuizAttemptORM.attempt_id)).where(
        QuizAttemptORM.status == Status.FINISHED
    )
    count_quizzes = await session.scalar(stmt)
    return count_quizzes


async def get_all_attempts(session: AsyncSession) -> int:
    stmt = select(func.count(QuizAttemptORM.attempt_id))
    count_attempts = await session.scalar(stmt)
    return count_attempts
