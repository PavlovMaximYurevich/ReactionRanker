import asyncio
import logging
import os

import aioschedule
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker
from handlers import router
from middlewares import DatabaseSession
from user_group import group_router

bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher()

# sheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# sheduler.add_job()

dispatcher.include_router(router)
dispatcher.include_router(group_router)


@dispatcher.message()
async def message_sheduler():

    await bot.send_message(chat_id='-1002084425436', text="Это сообщение будет генерироваться каждые 5 секунд")


async def scheduler():
    aioschedule.every(5).seconds.do(message_sheduler)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_start_up(bot: Bot):
    # run_param = False
    # if run_param:
    #     await drop_db()
    asyncio.create_task(scheduler())
    # jobs = [asyncio.create_task(job.run()) for job in self.jobs if job.should_run]
    await create_db()





async def on_shutdown(bot):
    print('Бот не работает')


async def main():
    dispatcher.startup.register(on_start_up)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.update.middleware(DatabaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
