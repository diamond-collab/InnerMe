from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import AnswerOptionORM, QuizQuestionORM
from who_am_i.services.answer_options_constants import DEFAULT_ANSWER_OPTIONS


async def get_options_by_question_id(
    session: AsyncSession,
    question_id: int,
) -> list[AnswerOptionORM]:
    stmt = select(AnswerOptionORM).where(AnswerOptionORM.question_id == question_id)
    result = list((await session.scalars(stmt)).all())

    return result


async def get_option_by_id(
    session: AsyncSession,
    option_id: int,
) -> AnswerOptionORM | None:
    stmt = select(AnswerOptionORM).where(AnswerOptionORM.option_id == option_id)
    result = await session.scalar(stmt)
    return result


async def create_default_answer_options_for_questions(
    session: AsyncSession,
    questions: list[QuizQuestionORM],
) -> None:

    payload = list()
    for question in questions:
        for option in DEFAULT_ANSWER_OPTIONS:
            payload.append(
                {
                    'question_id': question.question_id,
                    'label': option['text'],
                    'value': option['value'],
                    'order': option['position'],
                }
            )
    stmt = insert(AnswerOptionORM).values(payload)
    await session.execute(stmt)
