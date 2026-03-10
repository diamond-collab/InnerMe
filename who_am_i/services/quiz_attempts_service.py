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
