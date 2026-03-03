from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.handlers.show_test import render_tests

router = Router()


@router.message(F.text == 'Тесты')
async def open_tests_from_menu(message: Message, session: AsyncSession) -> None:
    await render_tests(message=message, session=session)
