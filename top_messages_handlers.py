from typing import List

from aiogram import Router, Bot
from aiogram import F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from orm_top_messages import (orm_all_get_top_messages,
                              orm_get_messages_day)

top_msg = Router()


async def output_text_message(array: List, message: Message, bot: Bot):
    if array:
        id_message = array[0]
        count_reactions = array[-1]
        await message.answer(f'Это самое залайканное сообщение '
                             f'с количеством реакции {count_reactions}')
        await bot.forward_message(
            # chat_id='-4190301675',
            # chat_id='1127674418',
            chat_id=message.from_user.id,  # куда пересылается
            from_chat_id='-1002084425436',
            # from_chat_id='-4190301675',  # откуда пересылается
            # text='Это сообщение набрало максимальное количество реакции',
            # reply_to_message_id=total[0][0]
            message_id=id_message
        )
    else:
        await message.answer("За выбранный период нет данных")


@top_msg.message(F.text == "Статистика по сообщениям за всё время")
async def get_all_top_messages(message: Message, session: AsyncSession, bot: Bot):

    total = await orm_all_get_top_messages(session)
    await output_text_message(total, message, bot)


@top_msg.message(F.text == "Статистика по сообщениям за день")
async def get_top_messages_day(message: Message, session: AsyncSession, bot: Bot):

    total = await orm_get_messages_day(session)
    await output_text_message(total, message, bot)
