from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import UserORM
from who_am_i.repositories import user_repo


async def get_current_user(session: AsyncSession, telegram_id: int) -> UserORM | None:
    return await user_repo.get_by_telegram_id(session=session, telegram_id=telegram_id)


async def get_or_create_user(
    session: AsyncSession,
    *,
    telegram_id: int,
    username: str | None = None,
    age: int | None = None,
) -> UserORM:
    user = await user_repo.get_by_telegram_id(session=session, telegram_id=telegram_id)
    if user is not None:
        return user

    if username is None or age is None:
        raise ValueError('username and age are required to create a user')

    return await user_repo.create_user(
        session=session,
        telegram_id=telegram_id,
        username=username,
        age=age,
    )


async def create_user(
    session: AsyncSession,
    *,
    telegram_id: int,
    username: str,
    age: int,
) -> UserORM:
    user = await user_repo.create_user(
        session=session,
        telegram_id=telegram_id,
        username=username,
        age=age,
    )

    return user
