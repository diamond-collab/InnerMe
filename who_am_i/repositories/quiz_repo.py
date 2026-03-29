from sqlalchemy import select, update
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


async def get_quiz_by_id(session: AsyncSession, quiz_id: int) -> QuizORM | None:
    stmt = select(QuizORM).where(QuizORM.quiz_id == quiz_id)
    result = await session.scalar(stmt)
    return result


async def get_all_quizzes(session: AsyncSession) -> list[QuizORM]:
    stmt = select(QuizORM)
    result = list((await session.scalars(stmt)).all())
    return result


async def change_status_quiz_by_slug(
    session: AsyncSession,
    quiz_id: int,
    new_status: bool,
) -> QuizORM | None:
    quiz = await session.get(QuizORM, quiz_id)

    quiz.is_active = new_status
    await session.flush()
    return quiz


async def update_quiz_title_and_description(
    session: AsyncSession,
    text: str,
    slug: str,
    field: str,
) -> QuizORM | None:
    if field not in ('title', 'description'):
        return None

    stmt = (
        update(QuizORM)
        .where(
            QuizORM.slug == slug,
        )
        .values(**{field: text})
        .returning(QuizORM)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
