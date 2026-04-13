from typing import Any

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


async def create_questions(
    session: AsyncSession,
    questions: list[dict[str, Any]],
) -> list[QuizQuestionORM]:
    return await quiz_questions_repo.create_questions(
        session=session,
        questions=questions,
    )


async def get_max_questions_order_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> int | None:
    return await quiz_questions_repo.get_max_questions_order_by_quiz_id(
        session=session,
        quiz_id=quiz_id,
    )


async def update_question_reverse(
    session: AsyncSession,
    question_id: int,
    new_status_reverse: bool,
) -> QuizQuestionORM | None:
    return await quiz_questions_repo.update_question_reverse(
        session=session,
        question_id=question_id,
        new_status_reverse=new_status_reverse,
    )


async def change_status_by_question_id(
    session: AsyncSession,
    question_id: int,
    new_status: bool,
) -> QuizQuestionORM | None:
    return await quiz_questions_repo.change_status_by_question_id(
        session=session,
        question_id=question_id,
        new_status=new_status,
    )


async def get_question_by_question_id_and_edit_text(
    session: AsyncSession,
    question_id: int,
    text: str,
) -> QuizQuestionORM | None:
    return await quiz_questions_repo.get_question_by_question_id_and_edit_text(
        session=session,
        question_id=question_id,
        text=text,
    )
