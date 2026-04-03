import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import QuestionData, QuestionActionData
from who_am_i.services import quiz_questions_service
from who_am_i.bot.admin.views import render_edit_question, render_quiz_questions
from who_am_i.bot.admin.states import EditQuestionState


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(QuestionData.filter())
async def handler_render_question_card(
    callback: CallbackQuery,
    callback_data: QuestionData,
    session: AsyncSession,
):
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    if not question:
        await callback.answer('Ошибка! Попробуй позже')
        return

    await render_edit_question(
        callback=callback,
        question=question,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
    )


@router.callback_query(QuestionActionData.filter())
async def handle_question_actions(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    state: FSMContext,
    session: AsyncSession,
):

    action_map = {
        'edit_question': handler_edit_question_text,
        'edit_reverse': handler_edit_question_reverse,
        'toggle_active': handler_edit_question_active,
        'back_to_question': handler_back_to_question,
    }
    handler = action_map.get(callback_data.action)
    if handler is None:
        await callback.answer('Неизвестное действие')
        return
    logger.info(f'handler {handler}')
    if callback_data.action == 'edit_question':
        await handler(
            callback=callback,
            callback_data=callback_data,
            state=state,
        )
    else:
        await handler(
            callback=callback,
            callback_data=callback_data,
            session=session,
        )


@router.message(EditQuestionState.waiting_for_new_text_question)
async def handler_new_text_for_question(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    text = message.text.strip()
    if not text:
        await message.answer('Название вопроса не может быть пустым! Попробуй снова')
        return

    data = await state.get_data()
    question_id = data.get('question_id')
    quiz_id = data.get('quiz_id')
    page = data.get('page')

    updated_question = await quiz_questions_service.get_question_by_question_id_and_edit_text(
        session=session,
        question_id=question_id,
        text=text,
    )
    if updated_question is None:
        await message.answer('Не удалось обновить вопрос. Попробуй позже')
        return

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz_id,
    )

    if not questions:
        await message.answer('Не удалось загрузить вопросы теста')
        await state.clear()
        return

    await render_quiz_questions(
        event=message,
        quiz_id=quiz_id,  # type: ignore
        page=page,
        questions=questions,
    )
    await state.clear()


async def handler_edit_question_text(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    state: FSMContext,
):
    await callback.answer()
    await callback.message.answer('<b>Введи новое название вопроса</b>')

    await state.update_data(question_id=callback_data.question_id)
    await state.update_data(page=callback_data.page)
    await state.update_data(quiz_id=callback_data.quiz_id)

    await state.set_state(EditQuestionState.waiting_for_new_text_question)


async def handler_edit_question_reverse(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    await callback.answer()
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    if not question:
        await callback.answer('Ошибка! Попробуй позже')
        return

    new_status_reverse = not question.is_reverse
    updated_question = await quiz_questions_service.update_question_reverse(
        session=session,
        question_id=callback_data.question_id,
        new_status_reverse=new_status_reverse,
    )
    if updated_question is None:
        await callback.answer('Не удалось обновить reverse-статус')
        return

    await render_edit_question(
        callback=callback,
        question=updated_question,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
    )


async def handler_edit_question_active(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    await callback.answer()
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    if not question:
        await callback.answer('Ошибка! Попробуй позже')
        return

    new_status = not question.is_active
    updated_question = await quiz_questions_service.change_status_by_question_id(
        session=session,
        question_id=callback_data.question_id,
        new_status=new_status,
    )
    if updated_question is None:
        await callback.answer('Не удалось обновить статус вопроса')
        return

    await render_edit_question(
        callback=callback,
        question=updated_question,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
    )


async def handler_back_to_question(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    await callback.answer()
    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=callback_data.quiz_id,
    )
    await render_quiz_questions(
        event=callback,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
        questions=questions,
    )
