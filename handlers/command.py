from aiogram.types import Message

from misc import db, dp
from other import texts
from utils.keyboards import make_keyboard


@dp.message_handler(commands='start')
async def start(msg: Message):
    """Заносит пользователя в базу, обнуляет все данные, задает первый вопрос"""
    user_id = msg.from_user.id
    db.delete_user(user_id)
    db.insert_user({'id': user_id})
    await msg.answer(texts.start_msg)

    next_state = db.get_next_state(user_id)
    await msg.answer(next_state.question, reply_markup=make_keyboard(user_id, next_state))
