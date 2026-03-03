import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.handlers.show_test import render_tests

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command('test'))
async def handler_test(message: Message, session: AsyncSession) -> None:
    await render_tests(message=message, session=session)
