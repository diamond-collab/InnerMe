from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import AnswerOptionORM


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
