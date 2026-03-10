from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAttemptORM


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
