import logging

from aiogram import executor

import handlers
from misc import dp

# configure logger
logging.basicConfig(level=30, filename='logs/main.log', filemode='w',
                    format='\n%(asctime)s [%(levelname)s]\n%(msg)s')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
print(handlers)
