import asyncio
import logging
import os

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query import orm_get_statistics_week

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker, engine
from handlers import router, text_message_sheduler
from middlewares import DatabaseSession
from user_group import group_router

bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher()

dispatcher.include_router(router)
dispatcher.include_router(group_router)


async def message_sheduler():
    async with AsyncSession(engine) as session:
        total = await orm_get_statistics_week(session)
        # print('ЭТО РЕАКЦИИ ЗА НЕДЕЛЮ', total)
        text = await text_message_sheduler(total)
        # await bot.send_message(chat_id='-1002084425436', text="Это сообщение будет генерироваться каждые 5 секунд")
        await bot.send_message(chat_id='-1002084425436', text=text, parse_mode=ParseMode.HTML)


async def scheduler():
    aioschedule.every(10).seconds.do(message_sheduler)
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
