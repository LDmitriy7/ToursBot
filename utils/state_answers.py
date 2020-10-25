"""Приклепляет ответы к состояниям при импорте"""
from other.states import ALL_STATES, State
from misc import db
from os.path import dirname
import utils.api_adapter as api
from utils.inline_calendar import make_calendarIn, make_calendarTo


# главная функция
def get_answers(user_id: int, state: State, **kwargs):
    if callable(state.answers):
        return state.answers(user_id, **kwargs)
    return state.answers


# функции-ответы
def get_countries(*args):
    path = dirname(__file__)
    with open(f'{path}/../other/countries.txt') as fp:
        for row in fp:
            sign, name, c_id, flag = row.split('«**»')
            if sign == '+':
                name = f'{name} {flag.strip()}'
                yield name, c_id


def get_nights(*args):
    NIGHTS_AMOUNT = range(1, 22)
    return zip(NIGHTS_AMOUNT, NIGHTS_AMOUNT)


def get_nights_to(user_id):
    nights = int(db.select_user(user_id)['nights'])
    NIGHTS_AMOUNT = range(nights, min(nights + 3, 22))
    return zip(NIGHTS_AMOUNT, NIGHTS_AMOUNT)


def get_adults(*args):
    ADULTS_AMOUNT = range(1, 5)
    return zip(ADULTS_AMOUNT, ADULTS_AMOUNT)


def get_kid_ages(*args):
    KIDS_AGES = range(1, 18)
    yield 'Без ребенка', 'any'
    for i in KIDS_AGES:
        yield i, i


def get_food(*args):
    FOOD_CATEGORIES = ['ob', 'bb', 'hb', 'fb', 'ai', 'uai']
    for c in FOOD_CATEGORIES:
        yield c.upper(), c


def get_foodTo(user_id: int):
    FOOD_CATEGORIES = ['ob', 'bb', 'hb', 'fb', 'ai', 'uai']
    food = db.select_user(user_id)['food']
    foodTo = FOOD_CATEGORIES[FOOD_CATEGORIES.index(food):]
    for f in foodTo:
        yield f.upper(), f


def get_stars(*args):
    STARS = range(1, 6)
    return zip(STARS, STARS)


def get_startTo(user_id: int):
    stars = db.select_user(user_id)['stars']
    STARS = range(int(stars), 6)
    return zip(STARS, STARS)


def get_beach_lines(*args):
    yield '1-я линия', 1
    yield 'до 2-й линии', 2
    yield 'любая линия', 3


def get_price(*args):
    yield 'Задать цену ОТ', 'set_price'
    yield 'Любая', 'any'


def get_priceTo(*args):
    yield 'Задать цену ДО', 'set_priceTo'
    yield 'Любая', 'any'


# карта состояний и наборов ответов
states_map = {
    'country': get_countries,
    'city': api.get_cities,
    'from': api.get_fromCities,
    'checkIn': make_calendarIn,
    'checkTo': make_calendarTo,
    'nights': get_nights,
    'nightsTo': get_nights_to,
    'adults': get_adults,
    'kid1': get_kid_ages,
    'kid2': get_kid_ages,
    'kid3': get_kid_ages,
    'food': get_food,
    'foodTo': get_foodTo,
    'stars': get_stars,
    'starsTo': get_startTo,
    'beach_line': get_beach_lines,
    'price': get_price,
    'priceTo': get_priceTo,
}
assert len(states_map) == len(ALL_STATES)

# прикрепление ответов к состоянием
for st in ALL_STATES:
    st.answers = states_map[st.name]
