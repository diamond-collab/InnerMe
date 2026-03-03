from sqlalchemy import ForeignKey, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AnswerOptionORM(Base):
    __tablename__ = 'answer_options'
    __table_args__ = (
        UniqueConstraint(
            'question_id',
            'order',
            name='uq_answer_options_question_id_order',
        ),
        UniqueConstraint(
            'question_id',
            'value',
            name='uq_answer_options_question_id_value',
        ),
        CheckConstraint(
            '"order" BETWEEN 1 AND 4',
            name='ck_answer_options_order_1_4',
        ),
        CheckConstraint(
            'value BETWEEN 1 AND 4',
            name='ck_answer_options_value_1_4',
        ),
    )

    option_id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            'quiz_questions.question_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    order: Mapped[int] = mapped_column(
        nullable=False,
    )
    label: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    value: Mapped[int] = mapped_column(
        nullable=False,
    )
