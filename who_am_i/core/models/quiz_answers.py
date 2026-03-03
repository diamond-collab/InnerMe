from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuizAnswers(Base):
    __tablename__ = 'quiz_answers'
    __table_args__ = (
        UniqueConstraint(
            'attempt_id',
            'question_id',
            name='uq_quiz_answers_attempt_id_question_id',
        ),
        CheckConstraint(
            'value BETWEEN 1 AND 4',
            name='ck_quiz_answers_value',
        ),
    )

    answer_id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey(
            'quiz_attempts.attempt_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            'quiz_questions.question_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey(
            'answer_options.option_id',
            ondelete='RESTRICT',
        ),
        nullable=False,
        index=True,
    )
    value: Mapped[int] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
