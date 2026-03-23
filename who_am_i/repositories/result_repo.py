from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizResultRangeORM, QuizResultTextORM


async def get_result_range(
    session: AsyncSession,
    quiz_id: int,
    result_percent: int,
) -> QuizResultRangeORM | None:
    stmt = select(QuizResultRangeORM).where(
        QuizResultRangeORM.quiz_id == quiz_id,
        QuizResultRangeORM.min_percent <= result_percent,
        QuizResultRangeORM.max_percent >= result_percent,
    )
    result = await session.scalar(stmt)
    return result


async def get_active_result_texts_by_range_id(
    session: AsyncSession,
    range_id: int,
) -> list[tuple[QuizResultTextORM, QuizResultRangeORM]]:
    stmt = (
        select(QuizResultTextORM, QuizResultRangeORM)
        .join(
            QuizResultRangeORM,
            QuizResultTextORM.range_id == QuizResultRangeORM.range_id,
        )
        .where(
            QuizResultTextORM.range_id == range_id,
            QuizResultTextORM.is_active.is_(True),
        )
        .order_by(QuizResultTextORM.order)
    )
    result = await session.execute(stmt)
    rows = result.tuples().all()
    return list(rows)
