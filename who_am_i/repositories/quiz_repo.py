from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizORM


async def get_active_quizzes(session: AsyncSession) -> list[QuizORM]:
    stmt = select(QuizORM).where(QuizORM.is_active.is_(True))
    existing = list((await session.scalars(stmt)).all())
    existing.sort(key=lambda q: q.title)
    return existing


async def quiz_by_slug(session: AsyncSession, slug: str) -> QuizORM | None:
    stmt = select(QuizORM).where(QuizORM.slug == slug)
    result = await session.scalars(stmt)
    return result.one_or_none()
