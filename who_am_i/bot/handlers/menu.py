from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.views import show_test, show_stats

router = Router()


@router.message(F.text == 'Тесты')
async def open_tests_from_menu(message: Message, session: AsyncSession) -> None:
    await show_test.render_tests(message=message, session=session)


@router.message(F.text == 'Статистика')
async def open_stats_from_menu(message: Message, session: AsyncSession) -> None:
    await show_stats.render_stats(message=message, session=session)
