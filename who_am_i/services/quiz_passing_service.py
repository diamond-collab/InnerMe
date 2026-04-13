from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import (
    quiz_attempts_service,
    quiz_questions_service,
    quiz_service,
    user_service,
)
from who_am_i.core.models import QuizORM, QuizAttemptORM, QuizQuestionORM


@dataclass
class StartQuizResult:
    status: Literal[
        'quiz_not_found',
        'user_not_found',
        'attempt_in_progress',
        'quiz_empty',
        'started',
    ]
    quiz: QuizORM | None = None
    attempt: QuizAttemptORM | None = None
    first_question: QuizQuestionORM | None = None


async def start_quiz(
    session: AsyncSession,
    telegram_id: int,
    slug: str,
) -> StartQuizResult:
    quiz = await quiz_service.get_quiz_by_slug(session=session, slug=slug)
    if quiz is None:
        return StartQuizResult(status='quiz_not_found')

    user = await user_service.get_current_user(
        session=session,
        telegram_id=telegram_id,
    )
    if user is None:
        return StartQuizResult(status='user_not_found')

    in_progress_attempt = await quiz_attempts_service.get_in_progress_attempt(
        session=session,
        user_id=user.user_id,
        quiz_id=quiz.quiz_id,
    )
    if in_progress_attempt is not None:
        return StartQuizResult(
            status='attempt_in_progress',
            quiz=quiz,
            attempt=in_progress_attempt,
        )

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz.quiz_id,
    )
    if not questions:
        return StartQuizResult(
            status='quiz_empty',
            quiz=quiz,
        )

    attempt = await quiz_attempts_service.create_quiz_attempts(
        session=session,
        quiz_id=quiz.quiz_id,
        user_id=user.user_id,
    )

    return StartQuizResult(
        status='started',
        quiz=quiz,
        attempt=attempt,
        first_question=questions[0],
    )
