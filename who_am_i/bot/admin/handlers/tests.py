import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.keyboards import (
    TestsPageData,
    QuizData,
    EditQuizData,
    inline_edit_quiz_keyboard,
)
from who_am_i.services import quiz_service, quiz_questions_service
from who_am_i.bot.admin.views import render_quiz_questions, render_tests_list, render_quiz_card
from .edit_quiz import edit_quiz_title_and_description

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(TestsPageData.filter())
async def handle_pagination(
    callback: CallbackQuery,
    callback_data: TestsPageData,
    session: AsyncSession,
):
    page = callback_data.page

    quizzes = await quiz_service.get_all_quizzes(session=session)
    await render_tests_list(callback=callback, quizzes=quizzes, page=page)


@router.callback_query(QuizData.filter())
async def show_selected_quiz(
    callback: CallbackQuery,
    callback_data: QuizData,
    session: AsyncSession,
):
    await callback.answer()

    quiz = await quiz_service.get_quiz_by_slug(
        session=session,
        slug=callback_data.slug,
    )
    if not quiz:
        await callback.message.answer('Тест не найден, попробуй в другой раз')
        return

    await render_quiz_card(
        event=callback,
        quiz=quiz,
        page=callback_data.page,
    )


@router.callback_query(EditQuizData.filter())
async def edit_quiz_actions(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
    state: FSMContext,
):
    action_map = {
        'description': handle_description_action,
        'questions': handle_questions_action,
        'edit': handle_edit_action,
        'edit_title': edit_quiz_title_and_description,
        'edit_description': edit_quiz_title_and_description,
        'toggle': handle_toggle_action,
        'back': handle_back_action,
    }

    handler = action_map.get(callback_data.action)
    if handler is None:
        await callback.answer('Неизвестное дейтсвие')
        return

    if callback_data.action in ('edit_title', 'edit_description'):
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


async def handle_description_action(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
):
    pass


async def handle_questions_action(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
):
    await callback.answer()

    quiz = await quiz_service.get_quiz_by_slug(
        session=session,
        slug=callback_data.slug,
    )
    if not quiz:
        await callback.answer('Ошибка! Попробуй позже')
        return

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz.quiz_id,  # type: ignore
    )
    if not questions:
        await callback.message.answer('<b>Вопросов к данному тесту пока что нет</b>')
        return

    await render_quiz_questions(
        callback=callback,
        callback_data=callback_data,
        questions=questions,
    )


async def handle_edit_action(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
):
    quiz = await quiz_service.get_quiz_by_slug(
        session=session,
        slug=callback_data.slug,
    )
    if quiz is None:
        await callback.answer('Ошибка, попробуй позже')
        return

    await callback.message.edit_text(
        '<b>Выбери что хочешь отредактировать</b>',
        reply_markup=inline_edit_quiz_keyboard(
            slug=callback_data.slug,
            page=callback_data.page,
        ),
    )


async def handle_toggle_action(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
):
    await callback.answer()

    quiz = await quiz_service.get_quiz_by_slug(
        session=session,
        slug=callback_data.slug,
    )
    if not quiz:
        await callback.answer('Нет такого теста')
        return

    new_status = not quiz.is_active
    await quiz_service.change_status_quiz_by_slug(
        session=session,
        quiz_id=quiz.quiz_id,
        new_status=new_status,
    )
    update_quiz = await quiz_service.get_quiz_by_slug(
        session=session,
        slug=callback_data.slug,
    )
    await render_quiz_card(
        event=callback,
        quiz=update_quiz,
        page=callback_data.page,
    )


async def handle_back_action(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    session: AsyncSession,
):
    await callback.answer()
    page = callback_data.page
    quizzes = await quiz_service.get_all_quizzes(session=session)

    await render_tests_list(
        callback=callback,
        quizzes=quizzes,
        page=page,
    )
