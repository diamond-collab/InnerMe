from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from who_am_i.bot.admin.filters import IsAdmin
from who_am_i.bot.admin.keyboards import main_admin_menu_keyboard

router = Router()


@router.message(IsAdmin(), Command('admin'))
async def handler_admin(message: Message):
    await message.answer(
        '<b>👨‍💻Админ-панель\n\n📍Выбери дейтсиве:</b>',
        reply_markup=main_admin_menu_keyboard(),
    )
