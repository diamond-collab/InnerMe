from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizORM
from who_am_i.repositories import quiz_repo


async def get_active_quizzes(session: AsyncSession) -> list[QuizORM]:
    quizzes = await quiz_repo.get_active_quizzes(session=session)
    return quizzes


async def get_quiz_by_slug(session: AsyncSession, slug: str) -> QuizORM | None:
    quiz = await quiz_repo.quiz_by_slug(session=session, slug=slug)
    if quiz is None:
        return None

    return quiz


async def get_quiz_by_id(session: AsyncSession, quiz_id: int) -> QuizORM | None:
    return await quiz_repo.get_quiz_by_id(session=session, quiz_id=quiz_id)


async def get_all_quizzes(session: AsyncSession) -> list[QuizORM]:
    return await quiz_repo.get_all_quizzes(
        session=session,
    )


async def change_status_quiz_by_slug(
    session: AsyncSession, quiz_id: int, new_status: bool
) -> QuizORM | None:
    return await quiz_repo.change_status_quiz_by_slug(
        session=session,
        quiz_id=quiz_id,
        new_status=new_status,
    )


async def update_quiz_title_and_description(
    session: AsyncSession,
    text: str,
    quiz_id: int,
    field: str,
):
    return await quiz_repo.update_quiz_title_and_description(
        session=session,
        text=text,
        quiz_id=quiz_id,
        field=field,
    )


async def create_quiz(
    session: AsyncSession,
    slug: str,
    title: str,
    description: str,
) -> QuizORM:
    return await quiz_repo.create_quiz(
        session=session,
        slug=slug,
        title=title,
        description=description,
    )
