"""Модуль для запросов к апи на подбор туров"""
from misc import db
import requests
from config import OTPUSK_API_TOKEN

BASE_URL = 'https://export.otpusk.com/api/tours/search'
s = requests.session()
s.params.update(access_token=OTPUSK_API_TOKEN)


def get_search_json(user_id: int):
    u_data = db.select_user(user_id)
    params = s.params

    # города, страны
    country, city = u_data['country'], u_data['city']
    params['to'] = country if city == 'any' else city
    params['from'] = u_data['from']

    # даты, дни
    params['checkIn'] = u_data['checkIn']
    params['checkTo'] = u_data['checkTo']
    params['nights'] = u_data['nights']
    params['nightsTo'] = u_data['nightsTo']

    # люди
    people = u_data['adults']
    for kid in [u_data['kid1'], u_data['kid2'], u_data['kid3']]:
        if kid != 'any':
            if len(kid) == 1:
                kid = '0' + kid
            people += kid
    params['people'] = people

    # питание
    FOOD_CATEGORIES = ['ob', 'bb', 'hb', 'fb', 'ai', 'uai']
    f_ind1 = FOOD_CATEGORIES.index(u_data['food'])
    f_ind2 = FOOD_CATEGORIES.index(u_data['foodTo'])
    params['food'] = ','.join(FOOD_CATEGORIES[f_ind1:f_ind2 + 1])

    # категория отеля
    stars = int(u_data['stars'])
    starsTo = int(u_data['starsTo'])
    stars_range = map(str, range(stars, starsTo + 1))
    params['stars'] = ','.join(stars_range)

    # линия пляжа
    LINES = ['one_line_beach', 'two_line_beach', 'next_beach_line']
    lines = LINES[:int(u_data['beach_line'])]
    params['services'] = ','.join(lines)

    # цены
    price, priceTo = u_data['price'], u_data['priceTo']
    params['price'] = None if price == 'any' else price
    params['priceTo'] = None if priceTo == 'any' else priceTo

    resp = s.get(BASE_URL)
    print(resp.request.url)
    print(resp.json())
