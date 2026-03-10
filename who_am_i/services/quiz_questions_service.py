from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM
from who_am_i.repositories import quiz_questions_repo


async def get_questions_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> list[QuizQuestionORM]:
    questions = await quiz_questions_repo.get_questions_by_quiz_id(session, quiz_id)

    return questions
