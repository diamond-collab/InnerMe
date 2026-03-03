import enum
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Enum, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Status(enum.Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    CANCELLED = 'cancelled'


class QuizAttemptORM(Base):
    __tablename__ = 'quiz_attempts'
    __table_args__ = (
        CheckConstraint(
            'result_percent BETWEEN 0 AND 100',
            name='ck_attempt_percent_range',
        ),
    )

    attempt_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.user_id',
            ondelete='CASCADE',
        ),
        index=True,
        nullable=False,
    )
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey(
            'quizzes.quiz_id',
            ondelete='CASCADE',
        ),
        index=True,
        nullable=False,
    )
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name='quiz_attempt_status',
        ),
        nullable=False,
        default=Status.IN_PROGRESS,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    seed: Mapped[int] = mapped_column(
        nullable=False,
    )
    result_score: Mapped[int | None] = mapped_column(
        nullable=True,
    )
    result_percent: Mapped[int | None] = mapped_column(
        nullable=True,
    )
