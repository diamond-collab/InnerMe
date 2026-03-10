from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM


async def get_questions_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> list[QuizQuestionORM]:
    stmt = select(QuizQuestionORM).where(QuizQuestionORM.quiz_id == quiz_id)
    result = list((await session.scalars(stmt)).all())
    return result
