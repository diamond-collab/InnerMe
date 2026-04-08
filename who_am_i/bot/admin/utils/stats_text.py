from who_am_i.services.stats_service import CommonStats


def build_stats_text(
    stats: CommonStats,
) -> str:
    text = (
        f'<b>📊 Общая Статистика</b>\n'
        f'👤 Пользователей: {stats.users}\n'
        f'🧪 Пройдено тестов: {stats.finished_quizzes}\n'
        f'🔁 Всего попыток: {stats.attempts}\n\n'
        f'<i>👇 Посмотреть детальную статистику по тесту</i>'
    )
    return text
