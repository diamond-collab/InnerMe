import asyncio
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models.answer_options import AnswerOptionORM
from who_am_i.core.models.quizzes import QuizORM
from who_am_i.core.models.quiz_questions import QuizQuestionORM
from who_am_i.core.models.db_helper import db_helper

DATA_QUIZZES: dict = {
    'social_confidence': {
        'title': 'Тест на социальную уверенность',
        'description': 'Тест на социальную уверенность',
        'questions': [
            {
                'order': 1,
                'text': 'Мне легко заводить друзей.',
                'is_reverse': False,
                'dimension': 'E1',
            },
            {
                'order': 2,
                'text': 'Мне комфортно находиться среди людей.',
                'is_reverse': False,
                'dimension': 'E1',
            },
            {
                'order': 3,
                'text': 'Мне часто бывает некомфортно рядом с другими людьми.',
                'is_reverse': True,
                'dimension': 'E1',
            },
            {
                'order': 4,
                'text': 'Я стараюсь избегать контактов с другими людьми.',
                'is_reverse': True,
                'dimension': 'E1',
            },
            {
                'order': 5,
                'text': 'На мероприятиях я общаюсь с разными людьми.',
                'is_reverse': False,
                'dimension': 'E2',
            },
            {
                'order': 6,
                'text': 'Мне нравится работать или делать что-то в группе.',
                'is_reverse': False,
                'dimension': 'E2',
            },
            {
                'order': 7,
                'text': 'Я не люблю многолюдные мероприятия.',
                'is_reverse': True,
                'dimension': 'E2',
            },
            {
                'order': 8,
                'text': 'Я часто беру инициативу в свои руки.',
                'is_reverse': False,
                'dimension': 'E3',
            },
            {
                'order': 9,
                'text': 'Мне проще дождаться, пока другие возьмут на себя лидерство.',
                'is_reverse': True,
                'dimension': 'E3',
            },
            {
                'order': 10,
                'text': 'Мне не нравится привлекать к себе внимание.',
                'is_reverse': True,
                'dimension': 'E3',
            },
        ],
    },
    'self_esteem': {
        'title': 'Тест на самооценку',
        'description': 'Этот тест поможет определить, насколько устойчиво и уверенно ты '
        'воспринимаешь себя, свои качества и свою ценность. Ответь на несколько '
        'утверждений честно, ориентируясь на то, как ты обычно думаешь и чувствуешь в реальной жизни. В конце теста ты получишь результат и краткий разбор своего уровня самооценки.',
        'questions': [
            {
                'order': 1,
                'text': 'Мне комфортно быть собой.',
                'is_reverse': False,
                'dimension': 'SE1',
            },
            {
                'order': 2,
                'text': 'Я обычно верю в свой успех.',
                'is_reverse': False,
                'dimension': 'SE1',
            },
            {
                'order': 3,
                'text': 'У меня редко бывает подавленное настроение.',
                'is_reverse': False,
                'dimension': 'SE1',
            },
            {
                'order': 4,
                'text': 'Мне нравится брать ответственность за свои решения.',
                'is_reverse': False,
                'dimension': 'SE2',
            },
            {
                'order': 5,
                'text': 'Я хорошо понимаю свои сильные стороны.',
                'is_reverse': False,
                'dimension': 'SE2',
            },
            {
                'order': 6,
                'text': 'Я часто недоволен собой.',
                'is_reverse': True,
                'dimension': 'SE3',
            },
            {
                'order': 7,
                'text': 'Мне кажется, что я менее способен, чем большинство людей.',
                'is_reverse': True,
                'dimension': 'SE3',
            },
            {
                'order': 8,
                'text': 'Мне кажется, что в моей жизни не хватает ясного направления.',
                'is_reverse': True,
                'dimension': 'SE4',
            },
            {
                'order': 9,
                'text': 'Я часто сомневаюсь, что справляюсь со своими делами как следует.',
                'is_reverse': True,
                'dimension': 'SE4',
            },
            {
                'order': 10,
                'text': 'Мне кажется, что я плохо справляюсь с трудностями.',
                'is_reverse': True,
                'dimension': 'SE4',
            },
        ],
    },
}

DEFAULT_OPTIONS = [
    {'value': 1, 'label': 'Совсем не про меня'},
    {'value': 2, 'label': 'Скорее не про меня'},
    {'value': 3, 'label': 'Скорее про меня'},
    {'value': 4, 'label': 'Полностью про меня'},
]


async def seed_social_confidence() -> None:
    async with db_helper.session_factory() as session:
        try:
            for key, value in DATA_QUIZZES.items():
                quiz = await get_or_create_quiz(
                    session=session,
                    slug=key,
                    title=value['title'],
                    description=value['description'],
                )
                questions = await get_or_create_questions(
                    session=session,
                    quiz_id=quiz.quiz_id,
                    questions=value['questions'],
                )
                await get_or_create_options(
                    session=session,
                    questions=questions,
                )

            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise


async def create_quiz(
    session: AsyncSession,
    slug: str,
    title: str,
    description: str,
) -> QuizORM:
    quiz = QuizORM(
        slug=slug,
        title=title,
        description=description,
    )
    session.add(quiz)
    await session.flush()
    return quiz


async def get_or_create_quiz(
    session: AsyncSession,
    slug: str,
    title: str,
    description: str,
) -> QuizORM:
    stmt = select(QuizORM).where(QuizORM.slug == slug)
    result = await session.scalar(stmt)
    if result:
        return result

    return await create_quiz(
        session=session,
        slug=slug,
        title=title,
        description=description,
    )


async def create_quiz_questions(
    session: AsyncSession,
    quiz_id: int,
    questions: list[dict[str, Any]],
) -> list[QuizQuestionORM]:
    objs = list()
    for qu in questions:
        objs.append(
            QuizQuestionORM(
                quiz_id=quiz_id,
                order=qu['order'],
                text=qu['text'],
                is_reverse=qu['is_reverse'],
                dimension=qu['dimension'],
            )
        )
    session.add_all(objs)
    await session.flush()
    return objs


async def get_or_create_questions(
    session: AsyncSession,
    quiz_id: int,
    questions: list[dict[str, Any]],
) -> list[QuizQuestionORM]:
    stmt = select(QuizQuestionORM).where(QuizQuestionORM.quiz_id == quiz_id)
    existing = (await session.scalars(stmt)).all()

    existing_orders = {q.order for q in existing}
    to_create = list()
    for qu in questions:
        if qu['order'] in existing_orders:
            continue
        else:
            to_create.append(qu)

    if to_create:
        created = await create_quiz_questions(
            session=session,
            quiz_id=quiz_id,
            questions=to_create,
        )
        all_questions = [*existing, *created]
    else:
        all_questions = existing

    all_questions.sort(key=lambda q: q.order)
    return all_questions


async def create_answer_options(
    session: AsyncSession,
    question_id: int,
    options: list[dict[str, Any]],
) -> list[AnswerOptionORM]:
    objs = list()
    for idx, option in enumerate(options, start=1):
        objs.append(
            AnswerOptionORM(
                question_id=question_id,
                order=idx,
                label=option['label'],
                value=option['value'],
            )
        )

    session.add_all(objs)
    await session.flush()
    return objs


async def get_or_create_options(
    session: AsyncSession,
    questions: list[QuizQuestionORM],
) -> list[AnswerOptionORM]:
    all_options: list[AnswerOptionORM] = []

    for question in questions:
        stmt = select(AnswerOptionORM).where(AnswerOptionORM.question_id == question.question_id)
        existing = list((await session.scalars(stmt)).all())

        existing_values = {opt.value for opt in existing}
        to_create: list[dict[str, Any]] = []
        for option in DEFAULT_OPTIONS:
            if option['value'] in existing_values:
                continue
            to_create.append(option)

        if to_create:
            created = await create_answer_options(
                session=session,
                question_id=question.question_id,
                options=to_create,
            )
            per_question_options = [*existing, *created]
        else:
            per_question_options = existing

        per_question_options.sort(key=lambda opt: opt.value)
        all_options.extend(per_question_options)

    return all_options


if __name__ == '__main__':
    asyncio.run(seed_social_confidence())
