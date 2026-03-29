from .admin import router as admin_router
from .manage_quizzes import router as manage_quizzes_router
from .tests import router as test_router
from .edit_quiz import router as edit_quiz_router
from .edit_quiz import edit_quiz_title_and_description

__all__ = [
    'edit_quiz_title_and_description',
]


all_admin_routers = [
    admin_router,
    manage_quizzes_router,
    test_router,
    edit_quiz_router,
]
