from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuizResultTextORM(Base):
    __tablename__ = 'quiz_result_texts'
    __table_args__ = (UniqueConstraint('range_id', 'order', name='uq_quiz_result_text'),)

    text_id: Mapped[int] = mapped_column(primary_key=True)
    range_id: Mapped[int] = mapped_column(
        ForeignKey('quiz_result_ranges.range_id'),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    advice: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
