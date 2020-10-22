from aiogram.types import CallbackQuery

from misc import db, dp
from utils.keyboards import make_keyboard, search_keyboard


async def ask_next(user_id, query: CallbackQuery):
    """Задает следующий вопрос, редактируя сообщение"""
    next_state = db.get_next_state(user_id)
    msg = query.message
    if next_state is None:
        await msg.edit_text('Заявка заполнена', reply_markup=search_keyboard())
    else:
        await msg.edit_text(next_state.question, reply_markup=make_keyboard(user_id, next_state))


@dp.callback_query_handler(lambda query: query.data == 'back')
async def back(query: CallbackQuery):
    """Удаляет последнее заполненное поле"""
    user_id = query.from_user.id
    last_state = db.get_next_state(user_id, get_previous=True)
    if last_state is not None:
        db.update_user(user_id, {last_state.name: ''})
        await ask_next(user_id, query)
    await query.answer('Отменено')


@dp.callback_query_handler(lambda query: query.data == 'search')
async def search(query: CallbackQuery):
    """Начинает поиск результатов"""
    user_id = query.from_user.id
    next_state = db.get_next_state(user_id)
    if next_state is None:
        await query.answer('Ожидайте')
    else:
        await query.answer('Ответьте на все вопросы!')
        await ask_next(user_id, query)


@dp.callback_query_handler()
async def save_and_ask(query: CallbackQuery):
    """Сохраняет выбранные данные и заадает следующий вопрос"""
    user_id = query.from_user.id
    field, data = query.data.split(':')

    db.update_user(user_id, {field: data})
    await query.answer('Выбрано')
    await ask_next(user_id, query)
