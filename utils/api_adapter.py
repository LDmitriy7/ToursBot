"""Содержит функции, работающие конкретно с API otpusk.com"""
from misc import db
import requests
from config import OTPUSK_API_TOKEN

BASE_URL = 'https://export.otpusk.com/api/tours'
s = requests.session()
s.params.update(access_token=OTPUSK_API_TOKEN)


def get_cities(user_id: int):
    url = BASE_URL + '/cities'
    country = db.select_user(user_id)['country']
    resp = s.get(url, params={'countryId': country, 'with': 'price'})
    cities = resp.json()['cities']
    yield 'Любой', 'any'
    for c in cities:
        name, c_id = c['name'], c['id']
        yield name, c_id


def get_fromCities(user_id: int):
    url = BASE_URL + '/fromCities'
    country, city = db.select_user(user_id)[1:3]
    geo_id = country if city == 'any' else city
    resp = s.get(url, params={'geoId': geo_id})
    from_cities = resp.json()['fromCities']
    for c in from_cities:
        name, c_id = c['name'], c['id']
        yield name, c_id
