from sqlalchemy import select, func, distinct, desc
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import UserORM, QuizAttemptORM, Status, QuizResultRangeORM, QuizORM
from who_am_i.services.stats_service import PopularQuizStats


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


async def get_finished_quiz(session: AsyncSession, quiz_id: int) -> int:
    stmt = select(
        func.count(QuizAttemptORM.quiz_id),
    ).where(
        QuizAttemptORM.quiz_id == quiz_id,
        QuizAttemptORM.status == Status.FINISHED,
    )
    count_quiz = await session.scalar(stmt)
    return count_quiz


async def get_scores_finished_attempts(session: AsyncSession, quiz_id: int) -> list[QuizAttemptORM]:
    stmt = select(QuizAttemptORM).where(
        QuizAttemptORM.quiz_id == quiz_id,
        QuizAttemptORM.status == Status.FINISHED,
    )
    result = list((await session.scalars(stmt)).all())
    return result


async def get_finished_attempts_users(session: AsyncSession, quiz_id: int) -> int:
    stmt = select(func.count(distinct(QuizAttemptORM.user_id))).where(
        QuizAttemptORM.quiz_id == quiz_id,
        QuizAttemptORM.status == Status.FINISHED,
    )
    result = await session.scalar(stmt)
    return result


async def get_quiz_result_ranges(session: AsyncSession, quiz_id: int) -> list[QuizResultRangeORM]:
    stmt = select(QuizResultRangeORM).where(QuizResultRangeORM.quiz_id == quiz_id)
    return list((await session.scalars(stmt)).all())


async def get_popular_quizzes_stats(session: AsyncSession) -> list[PopularQuizStats]:
    stmt = (
        select(
            QuizORM.quiz_id,
            QuizORM.title,
            func.count(QuizAttemptORM.attempt_id).label('attempts_count'),
        )
        .join(QuizAttemptORM, QuizAttemptORM.quiz_id == QuizORM.quiz_id)
        .where(QuizAttemptORM.status == Status.FINISHED)
        .group_by(QuizORM.quiz_id, QuizORM.title)
        .order_by(desc(func.count(QuizAttemptORM.attempt_id)))
    )
    result = await session.execute(stmt)
    rows = result.all()

    return [
        PopularQuizStats(
            quiz_id=row.quiz_id,
            title=row.title,
            attempts_count=row.attempts_count,
        )
        for row in rows
    ]
