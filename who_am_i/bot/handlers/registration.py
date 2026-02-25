import logging
import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.states.states import RegisterUser
from who_am_i.services import user_service

logger = logging.getLogger(__name__)
router = Router()


@router.message(RegisterUser.input_username)
async def input_username(message: Message, state: FSMContext):
    text = message.text
    if not text:
        await message.answer('<i>Пожалуйста, отправь имя текстом 🙂</i>')
        return

    username = ' '.join(text.strip().split())
    logger.info('username: %s', username)

    pattern = r'^[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё -]{0,29}$'
    if not re.match(pattern, username):
        await message.answer(
            '<b>Имя должно содержать только буквы. Можно пробел или дефис. Попробуй ещё раз!</b>'
        )
        return

    await state.update_data(username=username)
    await state.set_state(RegisterUser.input_age)
    await message.answer('Записал 📝\n<i>Теперь введи свой возраст</i>')


@router.message(RegisterUser.input_age)
async def input_age(message: Message, state: FSMContext, session: AsyncSession) -> None:
    text = message.text
    if not text:
        await message.answer('<b>Пожалуйста, отправь возраст числом.</b>')
        return

    age_str = text.strip()
    if not age_str.isdigit():
        await message.answer('<b>Возраст должен быть числом. Например: 27</b>')
        return

    age = int(age_str)
    if not (1 <= age <= 120):
        await message.answer('<b>Возраст должен быть от 1 до 120.</b>')
        return

    data = await state.get_data()
    telegram_id = data.get('telegram_id')
    username = data.get('username')

    if telegram_id is None or username is None:
        await state.clear()
        await message.answer('<b>Что-то пошло не так. Нажми /start и начни заново.</b>')
        return

    await user_service.create_user(
        session=session,
        telegram_id=telegram_id,
        username=username,
        age=age,
    )

    await state.clear()
    await message.answer(f'<b>Регистрация завершена! <i>Привет, {username}</i></b>')
