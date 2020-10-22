from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from other.states import State
from utils.state_answers import get_answers


def make_keyboard(user_id: int, state: State):
    """Строит инлайн-клавиатуру на основе состояния"""
    keyboard = InlineKeyboardMarkup()
    for text, data in get_answers(user_id, state):
        button = InlineKeyboardButton(text, callback_data=f'{state.name}:{data}')
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return keyboard


def search_keyboard():
    """Строит клавиатуру для начала поиска"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('Начать поиск', callback_data='search'))
    keyboard.row(InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return keyboard
