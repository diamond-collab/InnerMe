import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.states import AddQuestionsState
from who_am_i.bot.admin.keyboards import inline_reverse_questions_keyboard, ReverseQuestionsData
from who_am_i.services import quiz_questions_service, answer_options_service
from who_am_i.bot.admin.views import render_quiz_questions

logger = logging.getLogger(__name__)

router = Router()


def build_questions_payload(
    quiz_id: int,
    start_order: int,
    questions: list[str],
    reverse_indexes: set[int],
) -> list[dict]:
    all_questions = []
    if start_order is None:
        start_order = 1
    else:
        start_order = start_order + 1

    for local_idx, question in enumerate(questions, start=1):
        order = start_order + local_idx - 1
        all_questions.append(
            {
                'quiz_id': quiz_id,
                'text': question,
                'is_reverse': local_idx in reverse_indexes,
                'order': order,
            }
        )
    return all_questions


@router.message(AddQuestionsState.waiting_for_questions)
async def add_questions(
    message: Message,
    state: FSMContext,
):
    text = message.text.strip().split('\n')
    await state.update_data(questions=text)

    formated_questions = list()
    for idx, question in enumerate(text, start=1):
        que = f'{idx}. {question}'
        formated_questions.append(que)

    result = '\n'.join(formated_questions)

    data = await state.get_data()
    quiz_id = data.get('quiz_id')
    page = data.get('page')

    kb = inline_reverse_questions_keyboard(quiz_id=quiz_id, page=page)
    await message.answer(
        f'<b>📋 Вот список вопросов:\n\n{result}\n\nЕсть ли среди них реверс-вопросы?</b>',
        reply_markup=kb,
    )


@router.callback_query(ReverseQuestionsData.filter())
async def check_reverse_questions(
    callback: CallbackQuery,
    callback_data: ReverseQuestionsData,
    state: FSMContext,
    session: AsyncSession,
):
    if callback_data.action == 'no':
        data = await state.get_data()
        quiz_id = data.get('quiz_id')
        questions = data.get('questions')
        page = data.get('page')

        start_order = await quiz_questions_service.get_max_questions_order_by_quiz_id(
            session=session,
            quiz_id=quiz_id,
        )
        logger.info(f'max_order: {start_order}')

        all_questions = build_questions_payload(
            quiz_id=quiz_id,
            start_order=start_order,
            questions=questions,
            reverse_indexes=set(),
        )

        created_question = await quiz_questions_service.create_questions(
            session=session,
            questions=all_questions,
        )
        await answer_options_service.create_default_answer_options_for_questions(
            session=session,
            questions=created_question,
        )

        new_questions = await quiz_questions_service.get_questions_by_quiz_id(
            session=session,
            quiz_id=quiz_id,
        )

        await render_quiz_questions(
            event=callback,
            quiz_id=quiz_id,
            page=page,
            questions=new_questions,
        )
    else:
        await callback.message.answer('Введи номера реверс вопросов через запятую')
        await state.set_state(AddQuestionsState.waiting_for_reverse_questions)


@router.message(AddQuestionsState.waiting_for_reverse_questions)
async def handle_reverse_questions(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    reverse = message.text.strip().split(',')
    reverse_idx = set(int(i) for i in reverse)

    data = await state.get_data()
    questions = data.get('questions')
    quiz_id = data.get('quiz_id')
    page = data.get('page')

    error_idx = list()
    for idx in reverse_idx:
        if idx < 1 or idx > len(questions):
            error_idx.append(str(idx))

    if error_idx:
        msg = ', '.join(error_idx)

        await message.answer(
            f'❌ Некорректные номера: {msg}\n'
            f'Допустимый диапазон: 1–{len(questions)}\n\n'
            f'Попробуй ещё раз'
        )
        return

    start_order = await quiz_questions_service.get_max_questions_order_by_quiz_id(
        session=session,
        quiz_id=quiz_id,
    )
    all_questions = build_questions_payload(
        quiz_id=quiz_id,
        start_order=start_order,
        questions=questions,
        reverse_indexes=reverse_idx,
    )

    created_question = await quiz_questions_service.create_questions(
        session=session,
        questions=all_questions,
    )
    await answer_options_service.create_default_answer_options_for_questions(
        session=session,
        questions=created_question,
    )

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz_id,
    )

    await render_quiz_questions(
        event=message,
        quiz_id=quiz_id,
        page=page,
        questions=questions,
    )
