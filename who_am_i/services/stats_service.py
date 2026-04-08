from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from who_am_i.core.models import QuizAttemptORM
from who_am_i.repositories import stats_repo


@dataclass
class CommonStats:
    users: int
    finished_quizzes: int
    attempts: int


async def get_common_stats(
    session: AsyncSession,
) -> CommonStats:
    users = await stats_repo.get_all_users(
        session=session,
    )
    finished_quizzes = await stats_repo.get_all_finished_quizzes(
        session=session,
    )
    attempts = await stats_repo.get_all_attempts(
        session=session,
    )

    return CommonStats(
        users=users,
        finished_quizzes=finished_quizzes,
        attempts=attempts,
    )


async def get_finished_quiz(
    session: AsyncSession,
    quiz_id: int,
) -> int:
    return await stats_repo.get_finished_quiz(
        session=session,
        quiz_id=quiz_id,
    )


async def get_scores_finished_attempts(
    session: AsyncSession,
    quiz_id: int,
) -> list[QuizAttemptORM]:
    return await stats_repo.get_scores_finished_attempts(
        session=session,
        quiz_id=quiz_id,
    )


async def get_finished_attempts_users(
    session: AsyncSession,
    quiz_id: int,
) -> int:
    return await stats_repo.get_finished_attempts_users(
        session=session,
        quiz_id=quiz_id,
    )
