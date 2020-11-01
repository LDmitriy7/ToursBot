"""Модуль для запросов к апи на подбор туров"""
from misc import db
import requests
from other.config import OTPUSK_API_TOKEN
from asyncio import sleep

BASE_URL = 'https://export.otpusk.com/api/tours/search'
PHOTO_URL = 'https://newimg.otpusk.com/3/800x600/'
s = requests.session()
s.params.update(access_token=OTPUSK_API_TOKEN)


def form_params(user_id: int, page):
    """Формирует параметры для запроса к API"""
    u_data = db.select_user(user_id)
    params = {}

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
    params['uniqueHotels'] = True
    params['group'] = 1
    return params


async def get_search_results(user_id: int, page):
    """Возвращает словари и ссылки на сайт для результатов"""
    params = form_params(user_id, page)
    for n in range(7):
        params['number'] = n
        resp = s.get(BASE_URL, params=params)
        r_data = resp.json()
        if r_data['lastResult']:
            print(resp.request.url)
            try:
                hotels = r_data['hotels'][str(page)]
                for r in parse_tours(hotels):
                    p = params
                    site_url = f'http://otpusk24.com.ua#!f={p["nights"]}&l={p["nights"]}&i={r["h_id"]}&hid={r["h_id"]}&p={p["people"]}&d={p["from"]}&oid={r["offer_id"]}&page=tour&c={p["checkIn"]}&v={p["checkIn"]}&o={p["food"]}'
                    yield r, site_url
            except (KeyError, TypeError):
                pass
            break
        else:
            await sleep(6)


def parse_tours(hotels_json):
    for h_id in hotels_json:
        r = {'h_id': h_id}
        try:
            r['hotel'] = hotels_json[h_id]
            hotel = r['hotel']
            r['country'] = hotel['c']['n']
            r['city'] = hotel['t']['n']
            r['stars'] = int(str(hotel['s'])[0])
            r['h_name'] = hotel['n']
            r['photo'] = PHOTO_URL + hotel['f']

            r['offers'] = hotel['offers']
            offers = r['offers']
            r['offer_id'] = min(offers, key=lambda o_id: offers[o_id]['pl'])
            offer = offers[r['offer_id']]

            r['price'] = offer['pl']
            r['food'] = offer['f']
            r['dept_city'] = offer['c']
            r['date'] = offer['d']
            r['nights'] = offer['n']
            r['adults'] = offer['a']
            r['kids'] = offer['h']

        except (KeyError, TypeError):
            continue

        yield r
