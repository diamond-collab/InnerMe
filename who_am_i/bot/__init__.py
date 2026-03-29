from aiogram import Router

from .handlers import all_routers
from who_am_i.bot.admin.handlers import all_admin_routers

main_router = Router(name='main_router')

for router in all_routers:
    main_router.include_router(router)

for router in all_admin_routers:
    main_router.include_router(router)
