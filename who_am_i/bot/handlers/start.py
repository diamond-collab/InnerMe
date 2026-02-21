import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart)
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(
        '<b>Привет👋\nЯ помогу тебе узнать себя по лучше. Выбери нужный раздел</b>'
    )

    telegram_id = message.from_user.id
    logger.info(f'telegram_id: {telegram_id}')

    await state.update_data(telegram_id=telegram_id)
