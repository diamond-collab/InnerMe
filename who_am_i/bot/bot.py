from who_am_i.core.config import settings
from who_am_i.core.logging import setup_logging

setup_logging(settings.logging)

import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from who_am_i.bot import main_router
from who_am_i.bot.middlewares.db_session import DBSessionMiddleware

logger = logging.getLogger(__name__)

bot = Bot(settings.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

dp.update.middleware(DBSessionMiddleware())

dp.include_router(main_router)


async def main():
    logger.info('Запуск бота...')
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f'Webhook удален, очередь обновлений сброшена')
    try:
        await dp.start_polling(bot)
    finally:
        logger.info('Бот завершил работу')


if __name__ == '__main__':
    asyncio.run(main())
