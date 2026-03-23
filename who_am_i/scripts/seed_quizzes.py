import asyncio
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from who_am_i.core.models.answer_options import AnswerOptionORM
from who_am_i.core.models.quizzes import QuizORM
from who_am_i.core.models.quiz_questions import QuizQuestionORM
from who_am_i.core.models import QuizResultTextORM, QuizResultRangeORM
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

RESULTS_DATA: dict = {
    'social_confidence': [
        {
            'order': 1,
            'min_percent': 0,
            'max_percent': 25,
            'title': 'Низкий уровень социальной уверенности',
            'texts': [
                {
                    'order': 1,
                    'description': 'Тебе может быть непросто чувствовать себя спокойно и свободно в общении с другими людьми. В новых компаниях, при знакомстве или в ситуациях, где нужно проявить себя, у тебя может быстро появляться напряжение, скованность или желание уйти в сторону. Скорее всего, ты часто внутренне оцениваешь себя в социальных ситуациях и переживаешь о том, как выглядишь в глазах окружающих.',
                    'advice': 'Начни с маленьких и безопасных шагов: чаще задавай короткие вопросы, поддерживай простые разговоры и не требуй от себя идеального поведения. Социальная уверенность растёт не от размышлений, а от повторяющегося опыта спокойного взаимодействия.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 2,
            'min_percent': 26,
            'max_percent': 50,
            'title': 'Умеренно сниженная социальная уверенность',
            'texts': [
                {
                    'order': 1,
                    'description': 'В целом ты способен общаться и включаться в контакт с людьми, но в напряжённых или непривычных ситуациях уверенность может быстро проседать. Иногда ты чувствуешь себя достаточно свободно, а иногда начинаешь сомневаться в себе, чрезмерно контролировать свои слова или переживать о впечатлении, которое производишь. Твоя уверенность ещё нестабильна и зависит от контекста, людей и внутреннего состояния.',
                    'advice': 'Полезно замечать не только неудачные, но и нормальные моменты общения. Попробуй чаще брать на себя небольшую инициативу: первым здороваться, задавать вопросы, поддерживать разговор хотя бы ещё на одну-две реплики дольше обычного.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 3,
            'min_percent': 51,
            'max_percent': 75,
            'title': 'Хороший уровень социальной уверенности',
            'texts': [
                {
                    'order': 1,
                    'description': 'Ты в целом достаточно уверенно чувствуешь себя в общении и умеешь входить в контакт с людьми без сильного внутреннего напряжения. Обычно ты способен выражать свои мысли, поддерживать разговор и не теряться в большинстве социальных ситуаций. При этом в новых, значимых или эмоционально насыщенных обстоятельствах у тебя всё ещё может появляться скованность, но она не мешает тебе полностью.',
                    'advice': 'Твоя задача сейчас не “исправлять себя”, а расширять зону комфорта. Полезно чаще практиковать инициативу в разговоре, учиться спокойнее переносить неловкие моменты и постепенно включаться в более сложные социальные ситуации.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 4,
            'min_percent': 76,
            'max_percent': 100,
            'title': 'Высокий уровень социальной уверенности',
            'texts': [
                {
                    'order': 1,
                    'description': 'Ты, скорее всего, чувствуешь себя свободно и устойчиво в общении с людьми. Тебе проще входить в контакт, выражать себя, поддерживать разговор и не зацикливаться на том, как именно тебя оценивают окружающие. Даже если в каких-то ситуациях ты волнуешься, это не лишает тебя способности действовать спокойно и уверенно.',
                    'advice': 'Хороший следующий шаг — использовать свою уверенность не только для комфорта, но и для роста. Например, чаще проявляй инициативу, тренируй публичное выражение мыслей и развивай навык спокойного лидерства в общении.',
                    'is_active': True,
                },
            ],
        },
    ],
    'self_esteem': [
        {
            'order': 1,
            'min_percent': 0,
            'max_percent': 25,
            'title': 'Низкий уровень самооценки',
            'texts': [
                {
                    'order': 1,
                    'description': 'Ты можешь довольно часто сомневаться в собственной ценности, способностях и праве на уверенность. Скорее всего, тебе трудно устойчиво опираться на свои сильные стороны, а внутренний критик нередко звучит громче, чем поддержка. В результате даже обычные ошибки, неудачи или сравнение с другими могут заметно бить по твоему состоянию и отношению к себе.',
                    'advice': 'Начни с восстановления более реалистичного отношения к себе: фиксируй свои сильные стороны, маленькие успехи и ситуации, где ты справился лучше, чем сам ожидал. Низкая самооценка меняется не за счёт “мотивации”, а через спокойное накопление фактов о собственной устойчивости и ценности.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 2,
            'min_percent': 26,
            'max_percent': 50,
            'title': 'Умеренно сниженная самооценка',
            'texts': [
                {
                    'order': 1,
                    'description': 'У тебя, вероятно, нет полного неприятия себя, но внутренняя уверенность в собственной ценности ещё недостаточно устойчива. Иногда ты можешь нормально воспринимать себя и свои качества, а иногда быстро уходить в сомнения, самообесценивание или сравнение с другими. Твоя самооценка пока сильно зависит от результатов, внешней оценки и текущего эмоционального состояния.',
                    'advice': 'Полезно учиться отделять свою ценность как человека от отдельных ошибок и неудач. Старайся чаще замечать, в чём ты уже силён, что умеешь делать хорошо и какие качества в себе реально можешь уважать.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 3,
            'min_percent': 51,
            'max_percent': 75,
            'title': 'Здоровая самооценка',
            'texts': [
                {
                    'order': 1,
                    'description': 'Ты в целом достаточно устойчиво воспринимаешь себя и свои качества. Скорее всего, ты способен видеть в себе не только слабые стороны, но и реальные достоинства, а ошибки не разрушают твоё отношение к себе полностью. Иногда сомнения могут появляться, но обычно они не захватывают тебя надолго и не мешают сохранять внутреннюю опору.',
                    'advice': 'Твоя задача сейчас — не столько поднимать самооценку, сколько укреплять её устойчивость. Полезно продолжать развивать самоуважение через действия, ответственность, заботу о себе и спокойное принятие своих ограничений без самоунижения.',
                    'is_active': True,
                },
            ],
        },
        {
            'order': 4,
            'min_percent': 76,
            'max_percent': 100,
            'title': 'Высокий уровень самооценки',
            'texts': [
                {
                    'order': 1,
                    'description': 'Ты, скорее всего, достаточно уверенно воспринимаешь себя, свои способности и свою ценность. У тебя есть внутренняя опора, которая позволяет не разрушаться из-за ошибок, неудач или чужой оценки. Такой результат обычно говорит о том, что ты умеешь относиться к себе с уважением, видеть свои сильные стороны и сохранять ощущение собственной значимости без постоянных внешних подтверждений.',
                    'advice': 'Главное — сохранять баланс между уверенностью и реалистичностью. Сильная самооценка особенно полезна тогда, когда она соединяется с открытостью к развитию, умением признавать ошибки и уважением к другим людям.',
                    'is_active': True,
                },
            ],
        },
    ],
}


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

                result_ranges_data = RESULTS_DATA.get(key, [])
                ranges = await get_or_create_result_ranges(
                    session=session,
                    quiz_id=quiz.quiz_id,
                    ranges_data=result_ranges_data,
                )
                await get_or_create_result_texts(
                    session=session,
                    ranges=ranges,
                    ranges_data=result_ranges_data,
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


async def create_result_ranges(
        session: AsyncSession,
        quiz_id: int,
        ranges_data: list[dict[str, Any]],
) -> list[QuizResultRangeORM]:
    objs: list[QuizResultRangeORM] = []
    for range_data in ranges_data:
        objs.append(
            QuizResultRangeORM(
                quiz_id=quiz_id,
                order=range_data['order'],
                min_percent=range_data['min_percent'],
                max_percent=range_data['max_percent'],
                title=range_data['title'],
            )
        )

    session.add_all(objs)
    await session.flush()
    return objs


async def get_or_create_result_ranges(
        session: AsyncSession,
        quiz_id: int,
        ranges_data: list[dict[str, Any]],
) -> list[QuizResultRangeORM]:
    stmt = select(QuizResultRangeORM).where(QuizResultRangeORM.quiz_id == quiz_id)
    existing = list((await session.scalars(stmt)).all())

    existing_orders = {range_obj.order for range_obj in existing}
    to_create: list[dict[str, Any]] = []
    for range_data in ranges_data:
        if range_data['order'] in existing_orders:
            continue
        to_create.append(range_data)

    if to_create:
        created = await create_result_ranges(
            session=session,
            quiz_id=quiz_id,
            ranges_data=to_create,
        )
        all_ranges = [*existing, *created]
    else:
        all_ranges = existing

    all_ranges.sort(key=lambda range_obj: range_obj.order)
    return all_ranges


async def create_result_texts(
        session: AsyncSession,
        range_id: int,
        texts: list[dict[str, Any]],
) -> list[QuizResultTextORM]:
    objs: list[QuizResultTextORM] = []
    for text_data in texts:
        objs.append(
            QuizResultTextORM(
                range_id=range_id,
                order=text_data['order'],
                description=text_data['description'],
                advice=text_data['advice'],
                is_active=text_data['is_active'],
            )
        )

    session.add_all(objs)
    await session.flush()
    return objs


async def get_or_create_result_texts(
        session: AsyncSession,
        ranges: list[QuizResultRangeORM],
        ranges_data: list[dict[str, Any]],
) -> list[QuizResultTextORM]:
    all_texts: list[QuizResultTextORM] = []

    ranges_data_by_order = {range_data['order']: range_data for range_data in ranges_data}

    for range_obj in ranges:
        range_data = ranges_data_by_order.get(range_obj.order)
        if range_data is None:
            continue

        texts_data = range_data.get('texts', [])

        stmt = select(QuizResultTextORM).where(QuizResultTextORM.range_id == range_obj.range_id)
        existing = list((await session.scalars(stmt)).all())

        existing_orders = {text_obj.order for text_obj in existing}
        to_create: list[dict[str, Any]] = []
        for text_data in texts_data:
            if text_data['order'] in existing_orders:
                continue
            to_create.append(text_data)

        if to_create:
            created = await create_result_texts(
                session=session,
                range_id=range_obj.range_id,
                texts=to_create,
            )
            per_range_texts = [*existing, *created]
        else:
            per_range_texts = existing

        per_range_texts.sort(key=lambda text_obj: text_obj.order)
        all_texts.extend(per_range_texts)

    return all_texts


if __name__ == '__main__':
    asyncio.run(seed_social_confidence())
