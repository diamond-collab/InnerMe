from sqlalchemy import ForeignKey, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuizResultRangeORM(Base):
    __tablename__ = 'quiz_result_ranges'
    __table_args__ = (
        UniqueConstraint(
            'quiz_id',
            'order',
            name='uq_quiz_range_order',
        ),
        CheckConstraint(
            'min_percent <= max_percent',
            name='ck_min_le_max',
        ),
        CheckConstraint(
            'min_percent >= 0 AND max_percent <= 100',
            name='ck_percent_bounds',
        ),
    )

    range_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey('quizzes.quiz_id'),
        nullable=False,
        index=True,
    )
    min_percent: Mapped[int] = mapped_column(nullable=False)
    max_percent: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)
