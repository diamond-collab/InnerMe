from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Text, DateTime, UniqueConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuizQuestionORM(Base):
    __tablename__ = 'quiz_questions'
    __table_args__ = (
        UniqueConstraint(
            'quiz_id',
            'order',
            name='uq_quiz_id_order',
        ),
    )

    question_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey(
            'quizzes.quiz_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    order: Mapped[int] = mapped_column(
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    is_reverse: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )
    dimension: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
