from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.repositories import stats_repo
from who_am_i.services.stats_entities import CommonStats, QuizStats, PopularQuizStats


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


async def get_quiz_stats(
    session: AsyncSession,
    quiz_id: int,
) -> QuizStats | None:
    attempt_scores = await stats_repo.get_scores_finished_attempts(
        session=session,
        quiz_id=quiz_id,
    )
    if not attempt_scores:
        return None

    total_attempts = len(attempt_scores)
    unique_users = await stats_repo.get_finished_attempts_users(
        session=session,
        quiz_id=quiz_id,
    )
    total_score = sum(attempt.result_score for attempt in attempt_scores)
    avg_result = int(total_score / total_attempts)

    return QuizStats(
        total_attempts=total_attempts,
        unique_users=unique_users,
        avg_result=avg_result,
    )


async def get_quiz_result_ranges(
    session: AsyncSession,
    quiz_id: int,
) -> list[dict[str, Any]] | None:
    ranges = await stats_repo.get_quiz_result_ranges(
        session=session,
        quiz_id=quiz_id,
    )
    if not ranges:
        return None

    attempt_scores = await stats_repo.get_scores_finished_attempts(
        session=session,
        quiz_id=quiz_id,
    )
    if not attempt_scores:
        return None

    distribution = {r.title: 0 for r in ranges}

    ranges = sorted(ranges, key=lambda r: r.min_percent)

    for attempt in attempt_scores:
        for r in ranges:
            if r.min_percent <= attempt.result_percent <= r.max_percent:
                distribution[r.title] += 1
                break

    result = list()
    for r in ranges:
        result.append(
            {
                'title': r.title,
                'min': r.min_percent,
                'max': r.max_percent,
                'count': distribution[r.title],
            }
        )

    return result


async def get_popular_quiz_stats(
    session: AsyncSession,
) -> list[PopularQuizStats] | None:
    popular_quiz = await stats_repo.get_popular_quizzes_stats(
        session=session,
    )
    if not popular_quiz:
        return None

    return popular_quiz
