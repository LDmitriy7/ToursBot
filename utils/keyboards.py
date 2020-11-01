"""Набор клавиатур для бота"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from other.states import State
from utils.state_answers import get_answers


def make_keyboard(user_id: int, state: State):
    """Строит инлайн-клавиатуру на основе состояния"""
    if state.name in ['checkIn', 'checkTo']:
        return make_calendar(user_id, state)

    keyboard = InlineKeyboardMarkup()
    for text, data in get_answers(user_id, state):
        button = InlineKeyboardButton(text, callback_data=f'{state.name}:{data}')
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return keyboard


def search_keyboard(page=1):
    """Строит клавиатуру для начала поиска"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('Начать поиск', callback_data=f'search:{page}'))
    keyboard.row(InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return keyboard


def make_calendar(user_id: int, state: State, year_month: str = None):
    keyboard = InlineKeyboardMarkup(7)

    answers = list(get_answers(user_id, state, year_month=year_month))
    first_line = answers[:3]
    days_of_week = answers[3:10]
    days = answers[10:]

    keyboard.row(*[InlineKeyboardButton(text, callback_data=f'{state.name}:{data}') for text, data in first_line])
    keyboard.row(*[InlineKeyboardButton(text, callback_data=f'{state.name}:{data}') for text, data in days_of_week])

    for text, data in days:
        button = InlineKeyboardButton(text, callback_data=f'{state.name}:{data}')
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return keyboard


def results_keyboard(url, offer_id):
    keyboard = InlineKeyboardMarkup()
    manager_button = InlineKeyboardButton('Задать вопрос', callback_data=f'ask_manager:{offer_id}')
    site_button = InlineKeyboardButton('На сайт', url=url)
    keyboard.insert(manager_button)
    keyboard.insert(site_button)
    return keyboard
