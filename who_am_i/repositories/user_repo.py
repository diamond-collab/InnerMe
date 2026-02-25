from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import UserORM


async def get_by_telegram_id(session: AsyncSession, telegram_id: int) -> UserORM | None:
    result = await session.execute(select(UserORM).where(UserORM.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str,
    age: int,
) -> UserORM:
    user = UserORM(
        telegram_id=telegram_id,
        username=username,
        age=age,
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)

    return user
