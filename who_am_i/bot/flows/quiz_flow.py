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
    quiz_passing_service,
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
    result = await quiz_passing_service.start_quiz(
        session=session,
        telegram_id=callback.from_user.id,
        slug=slug,
    )

    await callback.answer()

    if result.status == 'quiz_not_found':
        await callback.message.answer('Тест пока что недоступен')
        return

    if result.status == 'user_not_found':
        await callback.message.answer('Пользователь не найден')
        return

    if result.status == 'attempt_in_progress':
        await callback.message.answer(
            f'У тебя есть незавершённый тест «{result.quiz.title}».\n'
            f'Хочешь продолжить его или начать заново?',
            reply_markup=build_progress_keyboard(result.attempt.attempt_id),
        )
        return

    if result.status == 'quiz_empty':
        await callback.message.answer('Тест находится в разработке')
        return

    await callback.message.answer(f'{result.quiz.description}\n\n')
    await send_quiz_question(
        session=session,
        question=result.first_question,
        attempt_id=result.attempt.attempt_id,
        callback=callback,
    )


async def handle_quiz_answer(
    callback: CallbackQuery,
    attempt_id: int,
    question_id: int,
    option_id: int,
    session: AsyncSession,
) -> None:

    result = await quiz_passing_service.submit_answer(
        session=session,
        attempt_id=attempt_id,
        question_id=question_id,
        option_id=option_id,
    )

    if result.status == 'question_not_found':
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось загрузить следующий вопрос.</b>\nПопробуй начать тест заново.'
        )
        return

    if result.status == 'option_not_found':
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось обработать выбранный ответ.</b>\nПопробуй выбрать вариант ещё раз.'
        )
        return

    if result.status == 'already_answered':
        await callback.answer('Ты ответил уже на этот вопрос')
        return

    if result.status == 'attempt_not_found':
        await callback.answer()
        await callback.message.answer(
            'Похоже, эта попытка теста уже завершена.\nВыбери тест заново.'
        )
        return

    await callback.message.edit_text(
        f'<b><i>❔Вопрос: {result.question.text}</i></b>\n\n'
        f'<i>✅ Твой ответ: {result.selected_option_label}</i>'
    )

    if result.status == 'next_question':
        await send_quiz_question(
            session=session,
            question=result.next_question,
            attempt_id=attempt_id,
            callback=callback,
        )
        return

    finish_result = result.finish_result
    if finish_result is None:
        await callback.answer()
        await callback.message.answer(
            '<b>Не удалось завершить тест.</b>\nПопробуй пройти его заново.'
        )
        return

    await callback.answer()

    advice_text = ''
    if finish_result.advice:
        advice_text = f'\n\n<b>Рекомендация:</b>\n\n{finish_result.advice}'

    if finish_result.level_title is None or finish_result.description is None:
        await callback.message.answer(
            f'<b>Результат теста</b>\n\n'
            f'Твой результат: <b>{finish_result.result_score}</b> '
            f'({finish_result.result_percent}%)\n\n'
            f'Пока для этого результата нет подробного описания.'
        )
        return

    await callback.message.answer(
        f'<b>Результат теста</b>\n\n'
        f'Твой результат: <b>{finish_result.result_score}</b> '
        f'({finish_result.result_percent}%)\n\n'
        f'<b>Уровень:</b> {finish_result.level_title}\n\n'
        f'<b>Описание:</b>\n\n{finish_result.description}{advice_text}'
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
