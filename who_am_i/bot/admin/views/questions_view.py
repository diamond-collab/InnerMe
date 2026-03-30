from aiogram.types import CallbackQuery

from who_am_i.bot.admin.keyboards import inline_back_to_quiz_keyboard, EditQuizData
from who_am_i.bot.admin.utils import questions_text
from who_am_i.core.models import QuizQuestionORM


async def render_quiz_questions(
    callback: CallbackQuery,
    callback_data: EditQuizData,
    questions: list[QuizQuestionORM],
):
    text = questions_text.build_questions_text(
        questions=questions,
    )
    await callback.message.edit_text(
        f'<b>❓ Всего вопросов: {len(questions)}</b>\n\n{text}',
        reply_markup=inline_back_to_quiz_keyboard(
            quiz_id=callback_data.quiz_id,
            page=callback_data.page,
        ),
    )
