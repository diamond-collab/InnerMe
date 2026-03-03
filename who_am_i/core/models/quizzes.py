from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuizORM(Base):
    __tablename__ = 'quizzes'

    quiz_id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    slug: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
