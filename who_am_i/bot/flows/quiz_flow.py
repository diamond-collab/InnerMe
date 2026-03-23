import logging

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.keyboards.inline_keyboard import build_progress_keyboard
from who_am_i.services import (
    answer_options_service,
    quiz_answers_service,
    quiz_attempts_service,
    quiz_questions_service,
    quiz_service,
    user_service,
)
from who_am_i.bot.flows.question_flow import send_quiz_question
from who_am_i.bot.flows.progress_flow import (
    get_attempt_or_notify,
    show_next_question_or_finish,
)

logger = logging.getLogger(__name__)


async def start_quiz(
    callback: CallbackQuery,
    slug: str,
    session: AsyncSession,
) -> None:
    quiz = await quiz_service.get_quiz_by_slug(session=session, slug=slug)
    if quiz is None:
        await callback.answer()
        await callback.message.answer('<b>Тест пока что недоступен</b>')
        return

    tg_id = callback.from_user.id
    user = await user_service.get_current_user(session=session, telegram_id=tg_id)
    if user is None:
        await callback.answer('<b>Пользователь не найден</b>')
        return

    in_progress_attempt = await quiz_attempts_service.get_in_progress_attempt(
        session=session,
        user_id=user.user_id,
        quiz_id=quiz.quiz_id,
    )
    if in_progress_attempt is not None:
        await callback.answer()
        await callback.message.answer(
            f'<b>У тебя есть незавершённый тест «{quiz.title}». Хочешь продолжить его '
            f'или начать заново?</b>',
            reply_markup=build_progress_keyboard(in_progress_attempt.attempt_id),
        )
        return

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz.quiz_id,
    )
    if not questions:
        await callback.answer('<b>Тест находится в разработке</b>')
        return

    attempt = await quiz_attempts_service.create_quiz_attempts(
        session=session,
        quiz_id=quiz.quiz_id,
        user_id=user.user_id,
    )

    first_question = questions[0]

    await callback.message.answer(f'{quiz.description}\n\n')

    await send_quiz_question(
        session=session,
        question=first_question,
        attempt_id=attempt.attempt_id,
        callback=callback,
    )


async def handle_quiz_answer(
    callback: CallbackQuery,
    attempt_id: int,
    question_id: int,
    option_id: int,
    session: AsyncSession,
) -> None:
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=question_id,
    )
    if question is None:
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось загрузить следующий вопрос.</b>\nПопробуй начать тест заново.'
        )
        return

    selected_response = await answer_options_service.get_option_by_id(
        session=session,
        option_id=option_id,
    )
    if selected_response is None:
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось обработать выбранный ответ.</b>\nПопробуй выбрать вариант ещё раз.'
        )
        return

    check_answer = await quiz_answers_service.get_answer_by_attempt_and_question(
        session=session, attempt_id=attempt_id, question_id=question.question_id
    )
    if check_answer:
        await callback.answer('Ты ответил уже на этот вопрос')
        return

    value = selected_response.value
    if question.is_reverse:
        value = 5 - value

    await quiz_answers_service.create_quiz_answer(
        session=session,
        attempt_id=attempt_id,
        question_id=question.question_id,
        option_id=option_id,
        value=value,
    )

    await callback.message.edit_text(
        f'<b><i>❔Вопрос: {question.text}</i></b>\n\n<i>✅ Твой ответ: {selected_response.label}</i>'
    )

    attempt = await get_attempt_or_notify(
        callback=callback,
        attempt_id=attempt_id,
        session=session,
    )
    if attempt is None:
        return

    next_order = question.order + 1
    await show_next_question_or_finish(
        callback=callback,
        attempt=attempt,
        next_order=next_order,
        session=session,
    )


async def restart_quiz(callback: CallbackQuery, attempt_id: int, session: AsyncSession) -> None:
    attempt = await get_attempt_or_notify(
        callback=callback,
        attempt_id=attempt_id,
        session=session,
    )
    if attempt is None:
        return
    await quiz_attempts_service.cancel_attempt(session=session, attempt_id=attempt_id)

    quiz = await quiz_service.get_quiz_by_id(
        session=session,
        quiz_id=attempt.quiz_id,
    )
    if quiz is None:
        await callback.answer()
        await callback.message.answer(
            '<b>Этот тест сейчас недоступен.</b>\nВыбери другой тест из списка.'
        )
        return

    await start_quiz(
        callback=callback,
        slug=quiz.slug,
        session=session,
    )


async def continue_quiz(
    callback: CallbackQuery,
    attempt_id: int,
    session: AsyncSession,
) -> None:
    attempt = await get_attempt_or_notify(
        callback=callback,
        attempt_id=attempt_id,
        session=session,
    )
    if attempt is None:
        return

    quiz_answers = await quiz_answers_service.get_quiz_answers_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    answered_count = len(quiz_answers)

    next_order = answered_count + 1
    await show_next_question_or_finish(
        callback=callback,
        attempt=attempt,
        next_order=next_order,
        session=session,
    )
