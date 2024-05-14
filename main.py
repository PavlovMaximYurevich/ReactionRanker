import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, MessageReactionCountUpdated

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker
from handlers import router
from middlewares import DatabaseSession
from user_group import group_router

# bot = Bot(token="6324678950:AAH7M6t8bo_9VrqTKzPWtRU8Lr81ezhbmd4")
bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher()

dispatcher.include_router(router)
dispatcher.include_router(group_router)


async def on_start_up(bot: Bot):
    # run_param = False
    # if run_param:
    #     await drop_db()
    await create_db()


async def on_shutdown(bot):
    print('Бот не работает')


async def main():
    dispatcher.startup.register(on_start_up)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.update.middleware(DatabaseSession(session_pool=session_maker))
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
