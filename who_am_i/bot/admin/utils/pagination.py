from who_am_i.core.models import QuizORM


async def pagination_of_buttons(
    quizzes: list[QuizORM],
    page: int,
) -> tuple[bool, bool, list[QuizORM]]:
    page_size = 5
    start = page * page_size
    end = start + page_size
    page_quizzes = quizzes[start:end]

    has_prev = page > 0
    has_next = end < len(quizzes)

    return has_prev, has_next, page_quizzes
