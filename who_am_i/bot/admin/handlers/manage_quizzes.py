from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.utils import pagination_of_buttons
from who_am_i.services import quiz_service
from who_am_i.bot.admin.keyboards import inline_build_tests_keyboard

router = Router()


@router.message(F.text == '📋 Тесты')
async def get_quizzes(message: Message, session: AsyncSession):
    quizzes = await quiz_service.get_all_quizzes(
        session=session,
    )
    if not quizzes:
        await message.answer(
            '<b>Пока что никаких тестов нет</b>\n\nДобавь первый тест нажава на '
            'кнопку <i>"Добавить тесты"</i></b>'
        )
        return

    page = 0
    has_prev, has_next, page_quizzes = await pagination_of_buttons(quizzes=quizzes, page=page)

    kb = inline_build_tests_keyboard(
        quizzes=page_quizzes,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
    )

    page_size = 5
    show_count = min((page + 1) * page_size, len(quizzes))
    await message.answer(
        '<b>📋 Управление тестами\n\n'
        'Выбери тест или действие.\n</b>'
        f'<i>Показано тестов: {show_count} из {len(quizzes)}</i>',
        reply_markup=kb,
    )
