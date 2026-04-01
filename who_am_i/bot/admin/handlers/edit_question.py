from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import QuestionData, QuestionActionData
from who_am_i.services import quiz_questions_service
from who_am_i.bot.admin.views import render_edit_question


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
    session: AsyncSession,
):

    action_map = {
        'edit_question': handler_edit_question_text,
        'edit_reverse': handler_edit_question_reverse,
        'edit_activ': handler_edit_question_active,
        'back_to_question': handler_back_to_question,
    }
    handler = action_map.get(callback_data.action)
    if handler is None:
        await callback.answer('Неизвестное действие')
        return

    await handler(
        callback=callback,
        callback_data=callback_data,
        session=session,
    )


async def handler_edit_question_text(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    pass


async def handler_edit_question_reverse(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    if not question:
        await callback.answer('Ошибка! Попробуй позже')
        return

    new_status_reverse = not question.is_reverse
    await quiz_questions_service.update_question_reverse(
        session=session,
        question_id=callback_data.question_id,
        new_status_reverse=new_status_reverse,
    )
    update_question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    await render_edit_question(
        callback=callback,
        question=update_question,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
    )


async def handler_edit_question_active(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    if not question:
        await callback.answer('Ошибка! Попробуй позже')
        return

    new_status = not question.is_active
    await quiz_questions_service.change_status_by_question_id(
        session=session,
        question_id=callback_data.question_id,
        new_status=new_status,
    )
    update_question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=callback_data.question_id,
    )
    await render_edit_question(
        callback=callback,
        question=update_question,
        quiz_id=callback_data.quiz_id,
        page=callback_data.page,
    )


async def handler_back_to_question(
    callback: CallbackQuery,
    callback_data: QuestionActionData,
    session: AsyncSession,
):
    pass
