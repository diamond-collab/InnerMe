from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

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
