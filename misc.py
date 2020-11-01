from os.path import dirname

from aiogram import Bot, Dispatcher

from other.config import BOT_TOKEN
from utils.sqlighter import DataBase

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

db_abs_dir = dirname(__file__)
db = DataBase(db_abs_dir + '/users.db')
