"""Содержит функции для state_answers, генерирующие данные календаря"""

from calendar import Calendar
from datetime import date, timedelta

from misc import db

DAYS_OF_WEEK = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
MONTHS = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']


def make_calendarIn(user_id: int, year_month: str = None):
    """Генерирует данные для календаря (CheckIn)"""
    if year_month:
        year, month = map(int, year_month.split('-'))
    else:
        today = str(date.today())
        year, month, _ = map(int, today.split('-'))

    from_date = date.today()
    to_date = from_date + timedelta(200)

    prev_m, next_m = get_prev_and_next_months(year, month)

    return iter_calendar(year, month, prev_m, next_m, from_date, to_date)


def make_calendarTo(user_id: int, year_month: str = None):
    """Генерирует данные для календаря (CheckTo)"""
    user_day = db.select_user(user_id)['checkIn']
    if year_month:
        year, month = map(int, year_month.split('-'))
    else:
        year, month, _ = map(int, user_day.split('-'))

    from_date = date.fromisoformat(user_day)
    to_date = from_date + timedelta(14)

    prev_m, next_m = get_prev_and_next_months(year, month)

    return iter_calendar(year, month, prev_m, next_m, from_date, to_date)


def iter_calendar(year, month, prev_m, next_m, from_date, to_date):
    """Итерирует все необходимые данные в правильном порядке"""
    yield '<', f'flip_to:{prev_m}'
    yield f'{MONTHS[month - 1]} {year}', 'error'
    yield '>', f'flip_to:{next_m}'

    for d in DAYS_OF_WEEK:
        yield d, 'error'

    for days7 in Calendar().monthdatescalendar(year, month):
        for day in days7:
            if from_date < day <= to_date and day.month == month:
                yield day.day, day
            else:
                yield ' ', 'error'


def get_prev_and_next_months(year: int, month: int) -> tuple:
    """Получить следующий и предыдущий месяцы в формате: ГГГГ-ММ"""
    cur_date = date(year, month, 15)
    prev_date = cur_date - timedelta(30)
    next_date = cur_date + timedelta(30)
    return f'{prev_date.year}-{prev_date.month}', f'{next_date.year}-{next_date.month}'
