from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.views import show_stats

router = Router()


@router.message(Command('stats'))
async def handler_stats(message: Message, session: AsyncSession) -> None:
    await show_stats.render_stats(message=message, session=session)
