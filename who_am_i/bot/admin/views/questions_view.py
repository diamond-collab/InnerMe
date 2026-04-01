from aiogram.types import CallbackQuery, Message

from who_am_i.bot.admin.keyboards import inline_questions_keyboard, build_question_actions_keyboard
from who_am_i.core.models import QuizQuestionORM


async def render_quiz_questions(
    event: CallbackQuery | Message,
    quiz_id: int,
    page: int,
    questions: list[QuizQuestionORM],
):
    if isinstance(event, CallbackQuery):
        if event.message is None:
            return
        await event.message.edit_text(
            f'<b>❓ Всего вопросов: {len(questions)}\n\nВыбери вопрос из спика</b>',
            reply_markup=inline_questions_keyboard(
                questions=questions,
                quiz_id=quiz_id,
                page=page,
            ),
        )
    elif isinstance(event, Message):
        await event.answer(
            f'<b>❓ Всего вопросов: {len(questions)}\n\nВыбери вопрос из спика</b>',
            reply_markup=inline_questions_keyboard(
                questions=questions,
                quiz_id=quiz_id,
                page=page,
            ),
        )


async def render_edit_question(
    callback: CallbackQuery,
    question: QuizQuestionORM,
    quiz_id: int,
    page: int,
):
    await callback.message.edit_text(
        f'❓ Вопрос №{question.order}.\n'
        f'📝 Название вопроса - {question.text}\n'
        f'Статус: {"✅ Активен" if question.is_active else "❌ Не активен"}\n'
        f'Обратный вопрос - {"🙃 Да" if question.is_reverse else "🙂 Нет"}',
        reply_markup=build_question_actions_keyboard(
            question_id=question.question_id,
            quiz_id=quiz_id,
            page=page,
        ),
    )
