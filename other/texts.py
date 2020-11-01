"""Содержит тексты и наборы строк для бота"""
from .dept_cities import dept_cities

start_msg = '''
Ответь на несколько вопросов бота, чтобы подобрать тур

В любой момент можно начать заполнение заново:
используй команду /start
'''

set_price = 'Введите цену ОТ (в гривнах):'
set_priceTo = 'Введите цену ДО (в гривнах):'


def search_results(country, city, h_name, stars, food, date, nights, dept_city, price, adults, kids, offer_id,
                   **kwargs):
    """Возвращает фото и текст для результата поиска"""

    result = f"""
{country}, {city}
🏨 {h_name} {stars * '⭐'}
🍽 Питание: {food.upper()}
🛫 {date} на {nights} {get_nights_word(nights)} из {dept_cities.get(dept_city, "")}
💰 {price} грн. за {adults} взр. + {kids} реб.
ID: {offer_id}
"""
    return result


def get_nights_word(nights):
    if int(nights) in [1, 21]:
        nights_word = 'ночь'
    elif int(nights) in [2, 3, 4]:
        nights_word = 'ночи'
    else:
        nights_word = 'ночей'
    return nights_word
