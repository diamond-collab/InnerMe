from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM
from who_am_i.repositories import quiz_questions_repo


async def get_questions_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> list[QuizQuestionORM]:
    questions = await quiz_questions_repo.get_questions_by_quiz_id(session, quiz_id)

    return questions


async def get_question_by_id(session: AsyncSession, question_id: int) -> QuizQuestionORM:
    question = await quiz_questions_repo.get_question_by_id(
        session=session, question_id=question_id
    )
    return question


async def get_question_by_id_and_order(
    session: AsyncSession,
    quiz_id: int,
    order: int,
) -> QuizQuestionORM:
    next_question = await quiz_questions_repo.get_question_by_id_and_order(
        session=session,
        quiz_id=quiz_id,
        order=order,
    )
    return next_question
