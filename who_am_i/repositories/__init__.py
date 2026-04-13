from .user_repo import get_by_telegram_id, create_user
from .quiz_repo import (
    get_active_quizzes,
    quiz_by_slug,
    get_quiz_by_id,
    get_all_quizzes,
    create_quiz,
)
from .quiz_attempts_repo import (
    create_quiz_attempt,
    update_quiz_attempt,
    get_attempt_by_id,
    get_finished_attempts_by_user_id,
    get_finished_attempts_with_quizzes_by_user_id,
    cancel_attempt,
)
from .quiz_questions_repo import (
    get_questions_by_quiz_id,
    get_question_by_id_and_order,
    create_questions,
    get_max_questions_order_by_quiz_id,
    update_question_reverse,
    change_status_by_question_id,
    get_question_by_question_id_and_edit_text,
)
from .answer_options_repo import (
    get_options_by_question_id,
    create_default_answer_options_for_questions,
)
from .quiz_answers_repo import (
    create_quiz_answer,
    get_quiz_answers_by_id,
    get_answer_by_attempt_and_question,
)
from .result_repo import get_result_range, get_active_result_texts_by_range_id

from .stats_repo import (
    get_all_users,
    get_all_finished_quizzes,
    get_all_attempts,
    get_finished_quiz,
    get_scores_finished_attempts,
    get_finished_attempts_users,
    get_quiz_result_ranges,
    get_popular_quizzes_stats,
)

__all__ = (
    'get_by_telegram_id',
    'create_user',
    'get_active_quizzes',
    'quiz_by_slug',
    'get_quiz_by_id',
    'get_all_quizzes',
    'create_quiz',
    'create_quiz_attempt',
    'get_answer_by_attempt_and_question',
    'update_quiz_attempt',
    'get_attempt_by_id',
    'get_finished_attempts_by_user_id',
    'get_finished_attempts_with_quizzes_by_user_id',
    'cancel_attempt',
    'get_questions_by_quiz_id',
    'get_question_by_id_and_order',
    'create_questions',
    'get_max_questions_order_by_quiz_id',
    'update_question_reverse',
    'change_status_by_question_id',
    'get_question_by_question_id_and_edit_text',
    'get_options_by_question_id',
    'create_default_answer_options_for_questions',
    'create_quiz_answer',
    'get_quiz_answers_by_id',
    'get_result_range',
    'get_active_result_texts_by_range_id',
    'get_all_users',
    'get_all_finished_quizzes',
    'get_all_attempts',
    'get_finished_quiz',
    'get_scores_finished_attempts',
    'get_finished_attempts_users',
    'get_quiz_result_ranges',
    'get_popular_quizzes_stats',
)
