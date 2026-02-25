import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.states.states import RegisterUser
from who_am_i.services import user_service

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart(), StateFilter(None))
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    telegram_id = message.from_user.id
    logger.info('Start command received | telegram_id=%s', telegram_id)

    user = await user_service.get_current_user(session=session, telegram_id=telegram_id)

    if user is None:
        await state.update_data(telegram_id=telegram_id)
        await state.set_state(RegisterUser.input_username)
        await message.answer(
            '<b>Вижу, что ты тут впервые. Пройди короткую регистрацию.</b>\n<i>Введи своё имя.</i>'
        )
        return

    await message.answer(f'<b>С Возвращением, {user.username}!</b>')


@router.message(CommandStart(), ~StateFilter(None))
async def start_during_registration(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    logger.info('Start during FSM | state=%s', current_state)

    await message.answer(
        '<b>Ты в процессе регистрации.\nПожалуйста, ответь на вопрос бота или отправь /cancel '
        'чтобы отменить.</b>'
    )


@router.message(Command('cancel'), ~StateFilter(None))
async def cancel_registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('<b>Регистрация отменена. Нажми /start чтобы начать заново.</b>')
