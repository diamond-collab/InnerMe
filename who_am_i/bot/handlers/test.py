from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.views import show_test
from who_am_i.bot.keyboards.inline_keyboard import QuizData, AnswerData, ProgressData
from who_am_i.bot.flows.quiz_flow import start_quiz, handle_quiz_answer, restart_quiz, continue_quiz

router = Router()


@router.message(Command('test'))
async def handler_test(message: Message, session: AsyncSession) -> None:
    await show_test.render_tests(message=message, session=session)


@router.callback_query(QuizData.filter())
async def handler_callback_query(
    callback: CallbackQuery,
    callback_data: QuizData,
    session: AsyncSession,
):
    await start_quiz(
        callback=callback,
        slug=callback_data.slug,
        session=session,
    )


@router.callback_query(AnswerData.filter())
async def handler_callback_query_answer(
    callback: CallbackQuery,
    callback_data: AnswerData,
    session: AsyncSession,
) -> None:
    await handle_quiz_answer(
        callback=callback,
        attempt_id=callback_data.attempt_id,
        question_id=callback_data.question_id,
        option_id=callback_data.option_id,
        session=session,
    )


@router.callback_query(ProgressData.filter())
async def handler_callback_query_progress(
    callback: CallbackQuery,
    callback_data: ProgressData,
    session: AsyncSession,
) -> None:
    action = callback_data.action
    if action == 'restart':
        await restart_quiz(
            callback=callback,
            attempt_id=callback_data.attempt_id,
            session=session,
        )
    else:
        await continue_quiz(
            callback=callback,
            attempt_id=callback_data.attempt_id,
            session=session,
        )
