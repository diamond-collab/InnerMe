def build_questions_text(questions) -> str:
    messages = list()
    for question in questions:
        msg = f'Вопрос №{question.order}\nОписание вопроса: {question.text}\n\n'
        messages.append(msg)

    return '\n'.join(messages)
