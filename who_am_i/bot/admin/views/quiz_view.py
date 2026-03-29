from aiogram.types import CallbackQuery, Message

from who_am_i.bot.admin.keyboards import build_quiz_actions_keyboard
from who_am_i.core.models import QuizORM


async def render_quiz_card(
    event: CallbackQuery | Message,
    quiz: QuizORM,
    page: int,
) -> None:
    created_at_text = quiz.created_at.strftime('%Y/%m/%d')
    text = (
        f'<b>🧩 {quiz.title}\n\n'
        f'<i>📌 Статус: {"✅Активен" if quiz.is_active else "❌ Неактивен"}\n'
        f'🕒 Добавлен: {created_at_text}\n\n</i></b>'
        f'<i>Описание теста: {quiz.description}</i>'
    )
    kb = build_quiz_actions_keyboard(quiz=quiz, page=page)

    if isinstance(event, CallbackQuery):
        if event.message is None:
            return
        await event.message.edit_text(text=text, reply_markup=kb)
    elif isinstance(event, Message):
        await event.answer(text, reply_markup=kb)
