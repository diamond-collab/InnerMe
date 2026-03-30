from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.bot.admin.states import AddQuizState
from who_am_i.bot.admin.utils import build_slug
from who_am_i.services import quiz_service
from who_am_i.bot.admin.views import render_quiz_card

router = Router()


@router.message(AddQuizState.waiting_for_title)
async def handle_input_title(
    message: Message,
    state: FSMContext,
) -> None:
    title = message.text.strip()
    slug = build_slug(text=title)

    await message.answer('<b>Записал\n</b><i>Теперь введи описание теста</i>')

    await state.update_data(slug=slug)
    await state.update_data(title=title)

    await state.set_state(AddQuizState.waiting_for_description)


@router.message(AddQuizState.waiting_for_description)
async def handle_input_description(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    description = message.text.strip()

    data = await state.get_data()
    base_slug = data.get('slug')
    title = data.get('title')

    slug = base_slug
    i = 2
    while await quiz_service.get_quiz_by_slug(session=session, slug=slug):
        slug = f'{base_slug}-{i}'
        i += 1

    quiz = await quiz_service.create_quiz(
        session=session,
        slug=slug,
        title=title,
        description=description,
    )

    await render_quiz_card(
        event=message,
        quiz=quiz,
        page=0,
    )
    await state.clear()
