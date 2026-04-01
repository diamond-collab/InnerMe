from aiogram.types import CallbackQuery, Message

from who_am_i.bot.admin.keyboards import inline_back_to_quiz_keyboard, EditQuizData
from who_am_i.bot.admin.utils import questions_text
from who_am_i.core.models import QuizQuestionORM


async def render_quiz_questions(
    event: CallbackQuery | Message,
    quiz_id: int,
    page: int,
    questions: list[QuizQuestionORM],
):
    text = questions_text.build_questions_text(
        questions=questions,
    )
    if isinstance(event, CallbackQuery):
        if event.message is None:
            return
        await event.message.edit_text(
            f'<b>❓ Всего вопросов: {len(questions)}</b>\n\n{text}',
            reply_markup=inline_back_to_quiz_keyboard(
                quiz_id=quiz_id,
                page=page,
            ),
        )
    elif isinstance(event, Message):
        await event.answer(
            text,
            reply_markup=inline_back_to_quiz_keyboard(
                quiz_id=quiz_id,
                page=page,
            ),
        )
