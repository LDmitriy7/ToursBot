"""Приклепляет ответы к состояниям при импорте"""
from other.states import ALL_STATES, State
from misc import db
from os.path import dirname
import utils.api_adapter as api


# главная функция
def get_answers(user_id: int, state: State):
    if callable(state.answers):
        return state.answers(user_id)
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


def get_adults(*args):
    ADULTS_AMOUNT = range(1, 5)
    return zip(ADULTS_AMOUNT, ADULTS_AMOUNT)


# прикрепление ответов к состоянием
for st in ALL_STATES:
    st.answers = get_adults

    states_map = {
        'country': get_countries,
        'city': api.get_city,
        'from': '',
        'checkIn': '',
        'checkTo': '',
        'nights': get_nights,
        'nightsTo': '',
        'adults': '',
        'kid1': '',
        'kid2': '',
        'kid3': '',
        'food': '',
        'foodTo': '',
        'stars': '',
        'starsTo': '',
        'price': '',
        'priceTo': '',
    }
    assert len(states_map) == len(ALL_STATES)

    if st.name == 'country':
        st.answers = states_map[st.name]

    print(repr(st.name))
