from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import EditQuizData
from who_am_i.bot.admin.states import EditState
from who_am_i.bot.admin.views import render_quiz_card
from who_am_i.services import quiz_service

router = Router()


async def edit_quiz_title_and_description(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    state: FSMContext,
):
    if callback_data.action == 'edit_title':
        await callback.message.answer('<i>Введи новое название теста</i>')
        await state.update_data(
            quiz_id=callback_data.quiz_id,
            page=callback_data.page,
            field='title',
        )
        await state.set_state(EditState.waiting_for_new_title)
    elif callback_data.action == 'edit_description':
        await callback.message.answer('<i>Введи новое описание теста</i>')
        await state.update_data(
            quiz_id=callback_data.quiz_id,
            page=callback_data.page,
            field='description',
        )
        await state.set_state(EditState.waiting_for_new_description)


@router.message(EditState.waiting_for_new_title)
async def edit_title(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    text = message.text.strip()
    data = await state.get_data()
    quiz_id = data.get('quiz_id')
    page = data.get('page')
    field = data.get('field')

    updated_quiz = await quiz_service.update_quiz_title_and_description(
        session=session,
        text=text,
        quiz_id=quiz_id,
        field=field,
    )
    if updated_quiz is None:
        await message.answer('Не удалось обновить тест')
        return

    await render_quiz_card(event=message, quiz=updated_quiz, page=page)
    await state.clear()


@router.message(EditState.waiting_for_new_description)
async def edit_description(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    text = message.text.strip()
    data = await state.get_data()
    quiz_id = data.get('quiz_id')
    page = data.get('page')
    field = data.get('field')

    updated_quiz = await quiz_service.update_quiz_title_and_description(
        session=session,
        text=text,
        quiz_id=quiz_id,
        field=field,
    )
    if updated_quiz is None:
        await message.answer('Не удалось обновить тест')
        return

    await render_quiz_card(event=message, quiz=updated_quiz, page=page)
    await state.clear()
