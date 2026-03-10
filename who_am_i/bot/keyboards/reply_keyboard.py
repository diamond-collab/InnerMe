from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Тесты'),
                KeyboardButton(text='ИИ тесты'),
            ],
            [
                KeyboardButton(text='Статистика'),
                KeyboardButton(text='Профиль'),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
