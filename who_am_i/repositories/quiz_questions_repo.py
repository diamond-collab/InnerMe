from typing import Any

from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM


async def get_questions_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> list[QuizQuestionORM]:
    stmt = select(QuizQuestionORM).where(QuizQuestionORM.quiz_id == quiz_id)
    result = list((await session.scalars(stmt)).all())
    return result


async def get_question_by_id(
    session: AsyncSession,
    question_id: int,
) -> QuizQuestionORM | None:
    stmt = select(QuizQuestionORM).where(QuizQuestionORM.question_id == question_id)
    result = await session.scalar(stmt)
    return result


async def get_question_by_id_and_order(
    session: AsyncSession,
    quiz_id: int,
    order: int,
) -> QuizQuestionORM | None:
    stmt = select(QuizQuestionORM).where(
        QuizQuestionORM.quiz_id == quiz_id,
        QuizQuestionORM.order == order,
    )
    result = await session.scalar(stmt)
    return result


async def create_questions(
    session: AsyncSession,
    questions: list[dict[str, Any]],
) -> None:
    stmt = insert(QuizQuestionORM).values(questions).returning(QuizQuestionORM)
    await session.execute(stmt)


async def get_max_questions_order_by_quiz_id(
    session: AsyncSession,
    quiz_id: int,
) -> int | None:
    stmt = select(func.max(QuizQuestionORM.order)).where(QuizQuestionORM.quiz_id == quiz_id)
    result = await session.scalar(stmt)
    return result


async def update_question_reverse(
    session: AsyncSession, question_id: int, new_status_reverse: bool
) -> QuizQuestionORM | None:
    question: QuizQuestionORM | None = await session.get(QuizQuestionORM, question_id)
    if question is None:
        return None
    question.is_reverse = new_status_reverse
    await session.flush()
    return question


async def change_status_by_question_id(
    session: AsyncSession,
    question_id: int,
    new_status: bool,
) -> QuizQuestionORM | None:
    question: QuizQuestionORM | None = await session.get(QuizQuestionORM, question_id)
    if question is None:
        return None
    question.is_active = new_status
    await session.flush()
    return question


async def get_question_by_question_id_and_edit_text(
    session: AsyncSession,
    question_id: int,
    text: str,
) -> QuizQuestionORM | None:
    question: QuizQuestionORM | None = await session.get(QuizQuestionORM, question_id)
    if question is None:
        return None
    question.text = text
    await session.flush()
    return question
