from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizORM
from who_am_i.repositories import quiz_repo


async def get_active_quizzes(session: AsyncSession) -> list[QuizORM]:
    quizzes = await quiz_repo.get_active_quizzes(session=session)
    return quizzes


async def get_quiz_by_slug(session: AsyncSession, slug: str) -> QuizORM | None:
    quiz = await quiz_repo.quiz_by_slug(session=session, slug=slug)
    if quiz is None:
        return None

    return quiz


async def get_quiz_by_id(session: AsyncSession, quiz_id: int) -> QuizORM | None:
    return await quiz_repo.get_quiz_by_id(session=session, quiz_id=quiz_id)
