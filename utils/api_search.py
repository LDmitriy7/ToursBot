"""Модуль для запросов к апи на подбор туров"""
from misc import db
import requests
from config import OTPUSK_API_TOKEN
from asyncio import sleep

BASE_URL = 'https://export.otpusk.com/api/tours/search'
PHOTO_URL = 'https://newimg.otpusk.com/3/800x600/'
s = requests.session()
s.params.update(access_token=OTPUSK_API_TOKEN)


def form_params(user_id: int, page):
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
    LINES = ['one_line_beach', 'two_line_beach']
    u_line = int(u_data['beach_line'])
    if u_line > 2:
        params['services'] = None
    else:
        lines = LINES[:u_line]
        params['services'] = ','.join(lines)

    # цены
    price, priceTo = u_data['price'], u_data['priceTo']
    params['price'] = None if price == 'any' else price
    params['priceTo'] = None if priceTo == 'any' else priceTo

    # прочее
    params['page'] = page
    return params


async def get_search_results(user_id: int, page):
    params = form_params(user_id, page)
    for n in range(7):
        resp = s.get(BASE_URL, params={'number': n})
        resp_data = resp.json()
        try:
            hotels = resp_data['hotels'][str(page)]
            for result in parse_tours(hotels):
                params['h_id'] = result[-1]
                params['offer_id'] = result[-2]
                yield result[:-1], params
        except (KeyError, TypeError):
            await sleep(6)
        if resp_data['lastResult']:
            print(resp.request.url)
            break


def parse_tours(hotels_json):
    for h_id in hotels_json:
        hotel = hotels_json[h_id]

        try:
            country = hotel['c']['n']
            city = hotel['t']['n']
            stars = int(hotel['s'])
            h_name = hotel['n']
            photo = PHOTO_URL + hotel['f']

            offers = hotel['offers']
            offer_id = min(offers, key=lambda o_id: offers[o_id]['pl'])
            offer = offers[offer_id]

            price = offer['pl']
            food = offer['f']
            dept_city = offer['c']
            date = offer['d']
            nights = offer['n']
            adults = offer['a']
            kids = offer['h']

        except (KeyError, TypeError):
            continue

        yield photo, country, city, h_name, stars, food, date, nights, dept_city, price, adults, kids, offer_id, h_id
