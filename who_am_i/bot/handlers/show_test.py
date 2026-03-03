from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import quiz_service
from who_am_i.bot.handlers.keyboards import build_quizzes_keyboard


async def render_tests(message: Message, session: AsyncSession) -> None:
    quizzes = await quiz_service.get_active_quizzes(session=session)
    kb = build_quizzes_keyboard(quizzes=quizzes)
    await message.answer('<b>Выбери тест который хочешь пройти 🤔</b>', reply_markup=kb)
