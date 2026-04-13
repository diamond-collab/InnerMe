from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import AnswerOptionORM, QuizQuestionORM
from who_am_i.repositories import answer_options_repo


async def get_options_by_question_id(
    session: AsyncSession,
    question_id: int,
) -> list[AnswerOptionORM]:
    return await answer_options_repo.get_options_by_question_id(
        session=session,
        question_id=question_id,
    )


async def get_option_by_id(
    session: AsyncSession,
    option_id: int,
) -> AnswerOptionORM | None:
    return await answer_options_repo.get_option_by_id(
        session=session,
        option_id=option_id,
    )


async def create_default_answer_options_for_questions(
    session: AsyncSession,
    questions: list[QuizQuestionORM],
) -> None:
    return await answer_options_repo.create_default_answer_options_for_questions(
        session=session,
        questions=questions,
    )
