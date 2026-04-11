from who_am_i.services.stats_entities import CommonStats


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


def build_popular_stats_text(
    items: list,
) -> str:
    return f'<b>🔥 Популярные тесты</b>\n\nВсего тестов: {len(items)}\n\n<i>Выбери тест 👇</i>'
