from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models import QuizQuestionORM
from who_am_i.services import answer_options_service
from who_am_i.bot.keyboards.inline_keyboard import build_answers_keyboard


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
    if not options:
        await callback.answer()
        await callback.message.answer(f'<b>Тест пока что недоступен</b>')
        return

    kb = build_answers_keyboard(
        options=options,
        attempt_id=attempt_id,
    )

    await callback.answer()

    await callback.message.answer(
        f'{question.text}',
        reply_markup=kb,
    )
