import asyncio

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.models import Poll, Question, Variant, Result
from tgbot.config import load_config


polls = [
    {
        "name": "Опросник тревожного расстройства ГТР-7 / GAD-7",
        "intro": "Оцени, насколько часто следующие проблемы беспокоили тебя последние две недели",
        "is_psychological": True,
        "questions": [
            {"content": "Чувство тревоги или раздражения"},
            {"content": "Неспособность справиться со своим беспокойством"},
            {"content": "Чрезмерное беспокойство по разным поводам"},
            {"content": "Неспособность расслабляться"},
            {"content": "Ощущение такого беспокойства, что трудно найти себе место"},
            {"content": "Склонность быстро испытывать злость или раздражительность"},
            {"content": "Чувство страха, как будто может случиться что–то ужасное"},
        ],
        "variants": [
            {"content": "Совсем нет", "points": 0},
            {"content": "В течение нескольких дней", "points": 1},
            {"content": "Более, чем половину этого времени", "points": 2},
            {"content": "Почти каждый день", "points": 3},
        ],
        "results": [
            {
                "content": "Минимальный уровень тревоги",
                "min_points": 0,
                "max_points": 4,
                "is_critical": False,
            },
            {
                "content": "Легкий уровень тревоги",
                "min_points": 5,
                "max_points": 9,
                "is_critical": False,
            },
            {
                "content": "Умеренная тревожность",
                "min_points": 10,
                "max_points": 14,
                "is_critical": False,
            },
            {
                "content": "Высокий уровень тревоги",
                "min_points": 15,
                "max_points": 100,
                "is_critical": True,
            },
        ],
    },
    {
        "name": "Шкала удовлетворенности жизнью (Satisfaction With Life Scale, SWLS)",
        "intro": "Ниже даны утверждения, с которыми вы можете согласиться или не согласиться.<br/>Выразите степень вашего согласия с каждым из них",
        "is_psychological": True,
        "questions": [
            {"content": "В основном моя жизнь близка к идеалу"},
            {"content": "Обстоятельства моей жизни исключительно благоприятны"},
            {"content": "Я полностью удовлетворен моей жизнью"},
            {"content": "У меня есть в жизни то, что мне по-настоящему нужно"},
            {"content": "Если бы мне пришлось жить еще раз, я бы оставил всё как есть"},
        ],
        "variants": [
            {"content": "Полностью не согласен", "points": 1},
            {"content": "Не согласен", "points": 2},
            {"content": "Скорее не согласен", "points": 3},
            {"content": "Нечто среднее", "points": 4},
            {"content": "Скорее согласен", "points": 5},
            {"content": "Согласен", "points": 6},
            {"content": "Полностью согласен", "points": 7},
        ],
        "results": [
            {"content": "ниже среднего", "min_points": 5, "max_points": 16, "is_critical": False},
            {
                "content": "среднее значение",
                "min_points": 17,
                "max_points": 24,
                "is_critical": False,
            },
            {"content": "выше среднего", "min_points": 25, "max_points": 35, "is_critical": True},
        ],
    },
    {
        "name": "Шкала воспринимаемого стресса, PSS-14",
        "intro": "Оцените, пожалуйста, как часто в течение последнего месяца вы испытывали те или иные мысли и чувства, используя предложенную шкалу ответов",
        "is_psychological": True,
        "questions": [
            {"content": "вы расстраивались из-за того, что происходило неожиданно?"},
            {
                "content": "вы чувствовали, что не способны контролировать важные моменты своей жизни?"
            },
            {"content": "вы нервничали и испытывали стресс?"},
            {"content": "вы успешно справлялись с нервировавшими вас жизненными трудностями?"},
            {
                "content": "вы эффективно справлялись с важными изменениями, происходящими в вашей жизни?"
            },
            {
                "content": "вы чувствовали уверенность в своей способности справляться с личными проблемами?"
            },
            {"content": "вы чувствовали, что всё идет так, как это нужно вам?"},
            {
                "content": "вы обнаруживали, что не можете справиться со всем, что вам приходилось делать?"
            },
            {"content": "вы могли контролировать свою раздражительность?"},
            {"content": "вы чувствовали, что находитесь на вершине успеха?"},
            {"content": "вы злились из-за того, что происходило без контроля с вашей стороны?"},
            {"content": "вы ловили себя на мыслях о том, что вам предстоит выполнить?"},
            {"content": "вы могли контролировать то, на что тратите свое время?"},
            {"content": "вы чувствовали, что вам не преодолеть всех скопившихся трудностей?"},
        ],
        "variants": [
            {"content": "Никогда", "points": 1},
            {"content": "Почти никогда", "points": 2},
            {"content": "Иногда", "points": 3},
            {"content": "Часто", "points": 4},
            {"content": "Очень часто", "points": 5},
        ],
        "results": [
            {
                "content": "низкий уровень стресса",
                "min_points": 0,
                "max_points": 15,
                "is_critical": False,
            },
            {
                "content": "средний уровень стресса",
                "min_points": 16,
                "max_points": 31,
                "is_critical": False,
            },
            {"content": "выше среднего", "min_points": 32, "max_points": 56, "is_critical": True},
        ],
    },
]


async def main():
    config = load_config(".env")
    async with create_session_pool(create_engine(config.db))() as session:
        for poll_data in polls:
            questions = poll_data.pop("questions")
            variants = poll_data.pop("variants")
            results = poll_data.pop("results")
            p = Poll(**poll_data)

            for q_data in questions:  # type: ignore
                q = Question(**q_data)
                for v_data in variants:  # type: ignore
                    v = Variant(**v_data)
                    q.variants.append(v)
                p.questions.append(q)

            for r_data in results:  # type: ignore
                r = Result(**r_data)
                p.results.append(r)

            session.add(p)
            await session.flush()
            await session.refresh(p)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
