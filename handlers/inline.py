from aiogram.types import CallbackQuery, ForceReply

from misc import db, dp, bot
from utils.keyboards import make_keyboard, search_keyboard, make_calendar, results_keyboard
import re
from other import texts
from utils.api_search import get_search_results
from asyncio import sleep
from config import PRIVATE_CHAT_ID


async def ask_next(user_id, query: CallbackQuery):
    """Задает следующий вопрос, редактируя сообщение"""
    next_state = db.get_next_state(user_id)
    msg = query.message
    if next_state is None:
        await msg.edit_text('Заявка заполнена', reply_markup=search_keyboard())
    else:
        await msg.edit_text(next_state.question, reply_markup=make_keyboard(user_id, next_state))


@dp.callback_query_handler(lambda query: re.search('ask_manager', query.data))
async def ask_manager(query: CallbackQuery):
    """Сообщает менеджерам о запросе"""
    user_id = query.from_user.id
    offer_id = query.data.split(':')[-1]
    await bot.send_message(user_id, 'Менеджер скоро свяжется с вами')
    await bot.send_message(PRIVATE_CHAT_ID, f'{user_id}: хочет задать вопрос по туру {offer_id}')


@dp.callback_query_handler(lambda query: re.search('error', query.data))
async def raise_error(query: CallbackQuery):
    """Сообщает об ошибке"""
    await query.answer('Ошибка')


@dp.callback_query_handler(lambda query: query.data == 'back')
async def back(query: CallbackQuery):
    """Удаляет последнее заполненное поле"""
    user_id = query.from_user.id
    last_state = db.get_next_state(user_id, get_previous=True)
    if last_state is not None:
        db.update_user(user_id, {last_state.name: ''})
        await ask_next(user_id, query)
    await query.answer('Отменено')


@dp.callback_query_handler(lambda query: re.search(r'flip_to:\d{4}-\d{1,2}$', query.data))
async def flip_calendar(query: CallbackQuery):
    user_id = query.from_user.id
    year_and_month = query.data.split(':')[-1]
    last_state = db.get_next_state(user_id)
    msg = query.message
    await msg.edit_text(msg.text, reply_markup=make_calendar(user_id, last_state, year_and_month))


@dp.callback_query_handler(lambda query: re.match(r'search:\d', query.data))
async def search(query: CallbackQuery):
    """Начинает поиск результатов"""
    user_id = query.from_user.id
    next_state = db.get_next_state(user_id)
    page = query.data.split(':')[-1]
    if next_state is None:
        await query.answer('Ожидайте')

        switcher = False
        async for result, params in get_search_results(user_id, page):
            await sleep(.5)
            switcher = True
            photo, text = texts.search_results(*result)
            await bot.send_photo(user_id, photo, text, reply_markup=results_keyboard(params))
        if switcher:
            await bot.send_message(user_id, 'Показать еще?', reply_markup=search_keyboard(int(page) + 1))
        else:
            await bot.send_message(user_id, 'Нет результатов')
    else:
        await query.answer('Ответьте на все вопросы!')
        await ask_next(user_id, query)


@dp.callback_query_handler(lambda query: re.search('set_price', query.data))
async def set_price(query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data.split(':')[-1]
    if data == 'set_price':
        await bot.send_message(user_id, texts.set_price, reply_markup=ForceReply())
    else:
        await bot.send_message(user_id, texts.set_priceTo, reply_markup=ForceReply())


@dp.callback_query_handler()
async def save_and_ask(query: CallbackQuery):
    """Сохраняет выбранные данные и заадает следующий вопрос"""
    user_id = query.from_user.id
    field, data = query.data.split(':')

    # пропускаем повторный выбор детей
    if field in ['kid1', 'kid2'] and data == 'any':
        db.update_user(user_id, {'kid3': 'any'})
        if field == 'kid1':
            db.update_user(user_id, {'kid2': 'any'})

    db.update_user(user_id, {field: data})
    await query.answer('Выбрано')
    await ask_next(user_id, query)
