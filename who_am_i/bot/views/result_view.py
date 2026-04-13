from who_am_i.services.quiz_passing_service import FinishQuizResult


def render_quiz_result_text(finish_result: FinishQuizResult) -> str:
    advice_text = ''
    if finish_result.advice:
        advice_text = f'\n\n<b>Рекомендация:</b>\n\n{finish_result.advice}'

    if finish_result.level_title is None or finish_result.description is None:
        return (
            f'<b>Результат теста</b>\n\n'
            f'Твой результат: <b>{finish_result.result_score}</b> '
            f'({finish_result.result_percent}%)\n\n'
            f'Пока для этого результата нет подробного описания.'
        )

    return (
        f'<b>Результат теста</b>\n\n'
        f'Твой результат: <b>{finish_result.result_score}</b> '
        f'({finish_result.result_percent}%)\n\n'
        f'<b>Уровень:</b> {finish_result.level_title}\n\n'
        f'<b>Описание:</b>\n\n{finish_result.description}{advice_text}'
    )
