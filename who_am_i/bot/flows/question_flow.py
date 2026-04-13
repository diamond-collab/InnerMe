import logging

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM
from who_am_i.services import answer_options_service
from who_am_i.bot.keyboards.inline_keyboard import build_answers_keyboard


logger = logging.getLogger(__name__)


async def send_quiz_question(
    session: AsyncSession,
    question: QuizQuestionORM,
    attempt_id: int,
    callback: CallbackQuery,
) -> None:
    options = await answer_options_service.get_options_by_question_id(
        session=session,
        question_id=question.question_id,
    )
    logger.info(f'options: {options}')
    if not options:
        await callback.answer()
        await callback.message.answer(f'<b>Тест пока что недоступен</b>')
        return

    logger.info(f'Option_id: {options[0].option_id}')
    logger.info(f'Question_id: {options[0].question_id}')
    logger.info(f'label: {options[0].label}')

    kb = build_answers_keyboard(
        options=options,
        attempt_id=attempt_id,
    )

    await callback.answer()

    await callback.message.answer(
        f'{question.text}',
        reply_markup=kb,
    )
