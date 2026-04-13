from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.services import (
    answer_options_service,
    quiz_answers_service,
    quiz_attempts_service,
    quiz_questions_service,
    quiz_service,
    result_service,
    user_service,
)
from who_am_i.core.models import QuizORM, QuizAttemptORM, QuizQuestionORM


@dataclass
class StartQuizResult:
    status: Literal[
        'quiz_not_found',
        'user_not_found',
        'attempt_in_progress',
        'quiz_empty',
        'started',
    ]
    quiz: QuizORM | None = None
    attempt: QuizAttemptORM | None = None
    first_question: QuizQuestionORM | None = None


@dataclass
class FinishQuizResult:
    attempt_id: int
    result_score: int
    result_percent: int
    level_title: str | None = None
    description: str | None = None
    advice: str | None = None


@dataclass
class SubmitAnswerResult:
    status: Literal[
        'question_not_found',
        'option_not_found',
        'already_answered',
        'attempt_not_found',
        'next_question',
        'finished',
    ]
    question: QuizQuestionORM | None = None
    selected_option_label: str | None = None
    next_question: QuizQuestionORM | None = None
    finish_result: FinishQuizResult | None = None


async def start_quiz(
    session: AsyncSession,
    telegram_id: int,
    slug: str,
) -> StartQuizResult:
    quiz = await quiz_service.get_quiz_by_slug(session=session, slug=slug)
    if quiz is None:
        return StartQuizResult(status='quiz_not_found')

    user = await user_service.get_current_user(
        session=session,
        telegram_id=telegram_id,
    )
    if user is None:
        return StartQuizResult(status='user_not_found')

    in_progress_attempt = await quiz_attempts_service.get_in_progress_attempt(
        session=session,
        user_id=user.user_id,
        quiz_id=quiz.quiz_id,
    )
    if in_progress_attempt is not None:
        return StartQuizResult(
            status='attempt_in_progress',
            quiz=quiz,
            attempt=in_progress_attempt,
        )

    questions = await quiz_questions_service.get_questions_by_quiz_id(
        session=session,
        quiz_id=quiz.quiz_id,
    )
    if not questions:
        return StartQuizResult(
            status='quiz_empty',
            quiz=quiz,
        )

    attempt = await quiz_attempts_service.create_quiz_attempts(
        session=session,
        quiz_id=quiz.quiz_id,
        user_id=user.user_id,
    )

    return StartQuizResult(
        status='started',
        quiz=quiz,
        attempt=attempt,
        first_question=questions[0],
    )


async def submit_answer(
    session: AsyncSession,
    attempt_id: int,
    question_id: int,
    option_id: int,
) -> SubmitAnswerResult:

    question = await quiz_questions_service.get_question_by_id(
        session=session,
        question_id=question_id,
    )
    if question is None:
        return SubmitAnswerResult(status='question_not_found')

    selected_option = await answer_options_service.get_option_by_id(
        session=session,
        option_id=option_id,
    )
    if selected_option is None:
        return SubmitAnswerResult(status='option_not_found')

    existing_answer = await quiz_answers_service.get_answer_by_attempt_and_question(
        session=session,
        attempt_id=attempt_id,
        question_id=question.question_id,
    )
    if existing_answer:
        return SubmitAnswerResult(
            status='already_answered',
            question=question,
            selected_option_label=selected_option.label,
        )

    value = selected_option.value
    if question.is_reverse:
        value = 5 - value

    await quiz_answers_service.create_quiz_answer(
        session=session,
        attempt_id=attempt_id,
        question_id=question.question_id,
        option_id=option_id,
        value=value,
    )

    attempt = await quiz_attempts_service.get_attempt_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if attempt is None:
        return SubmitAnswerResult(status='attempt_not_found')

    next_question = await quiz_questions_service.get_question_by_id_and_order(
        session=session,
        quiz_id=attempt.quiz_id,
        order=question.order + 1,
    )

    if next_question:
        return SubmitAnswerResult(
            status='next_question',
            question=question,
            selected_option_label=selected_option.label,
            next_question=next_question,
        )

    finish_result = await finish_attempt(
        session=session,
        attempt_id=attempt_id,
    )

    return SubmitAnswerResult(
        status='finished',
        question=question,
        selected_option_label=selected_option.label,
        finish_result=finish_result,
    )


async def finish_attempt(
    session: AsyncSession,
    attempt_id: int,
) -> FinishQuizResult | None:
    quiz_answers = await quiz_answers_service.get_quiz_answers_by_id(
        session=session,
        attempt_id=attempt_id,
    )
    if not quiz_answers:
        return None

    result_score = sum(answer.value for answer in quiz_answers)

    min_score = len(quiz_answers) * 1
    max_score = len(quiz_answers) * 4

    if max_score == min_score:
        result_percent = 0
    else:
        result_percent = round((result_score - min_score) / (max_score - min_score) * 100)

    quiz_attempt = await quiz_attempts_service.update_quiz_attempt(
        session=session,
        attempt_id=attempt_id,
        result_score=result_score,
        result_percent=result_percent,
    )
    if quiz_attempt is None:
        return None

    result = await result_service.get_result(
        session=session,
        quiz_id=quiz_attempt.quiz_id,
        result_percent=result_percent,
    )

    if result is None:
        return FinishQuizResult(
            attempt_id=attempt_id,
            result_score=result_score,
            result_percent=result_percent,
        )

    result_text, result_range = result

    return FinishQuizResult(
        attempt_id=attempt_id,
        result_score=result_score,
        result_percent=result_percent,
        level_title=result_range.title,
        description=result_text.description,
        advice=result_text.advice,
    )
