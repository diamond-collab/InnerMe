from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from who_am_i.core.config import settings


class IsAdmin(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user = event.from_user
        if user is None:
            return False
        return user.id in settings.admin_ids
