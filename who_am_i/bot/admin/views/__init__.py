from .tests_view import render_tests_list
from .questions_view import render_quiz_questions, render_edit_question
from .quiz_view import render_quiz_card
from .stats_quiz_view import render_quiz_list_stats

__all__ = [
    'render_tests_list',
    'render_quiz_questions',
    'render_quiz_card',
    'render_edit_question',
    'render_quiz_list_stats',
]
