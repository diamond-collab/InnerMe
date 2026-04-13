import random

from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizResultRangeORM, QuizResultTextORM
from who_am_i.repositories import result_repo


async def get_random_result_text(
    session: AsyncSession,
    range_id: int,
) -> tuple[QuizResultTextORM, QuizResultRangeORM] | None:
    result_texts = await result_repo.get_active_result_texts_by_range_id(
        session=session,
        range_id=range_id,
    )
    if not result_texts:
        return None

    if len(result_texts) == 1:
        return result_texts[0]

    return random.choice(result_texts)


async def get_result(
    session: AsyncSession,
    quiz_id: int,
    result_percent: int,
) -> tuple[QuizResultTextORM, QuizResultRangeORM] | None:
    quiz_result_range = await result_repo.get_result_range(
        session=session,
        quiz_id=quiz_id,
        result_percent=result_percent,
    )
    if not quiz_result_range:
        return None

    return await get_random_result_text(
        session=session,
        range_id=quiz_result_range.range_id,
    )
