from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizAttemptORM
from who_am_i.services import quiz_attempts_service


async def get_attempt_or_notify(
    callback: CallbackQuery,
    attempt_id: int,
    session: AsyncSession,
) -> QuizAttemptORM | None:
    attempt = await quiz_attempts_service.get_attempt_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if attempt is None:
        await callback.answer()
        await callback.message.answer(
            'Похоже, эта попытка теста уже завершена.\nВыбери тест заново.'
        )
        return None

    return attempt
