from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserORM(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str]
