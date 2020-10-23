from aiogram.types import Message

from misc import db, dp
from other import texts
from utils.keyboards import make_keyboard, search_keyboard


@dp.message_handler(commands='start')
async def start(msg: Message):
    """Заносит пользователя в базу, обнуляет все данные, задает первый вопрос"""
    user_id = msg.from_user.id
    db.delete_user(user_id)
    db.insert_user({'id': user_id})
    await msg.answer(texts.start_msg)

    next_state = db.get_next_state(user_id)
    await msg.answer(next_state.question, reply_markup=make_keyboard(user_id, next_state))


@dp.message_handler(lambda msg: msg.reply_to_message.text in [texts.set_price, texts.set_priceTo])
async def set_price(msg: Message):
    user_id = msg.from_user.id
    reply_text = msg.reply_to_message.text
    if reply_text == texts.set_price:
        field = 'price'
    else:
        field = 'priceTo'

    try:
        price = int(msg.text)
        db.update_user(user_id, {field: price})
        next_state = db.get_next_state(user_id)
        await msg.answer('Цена сохранена')

        if next_state is None:
            await msg.answer('Заявка заполнена', reply_markup=search_keyboard())
        else:
            await msg.answer(next_state.question, reply_markup=make_keyboard(user_id, next_state))

    except ValueError:
        await msg.answer('Ошибка, введите число')
