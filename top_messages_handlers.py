from typing import List

from aiogram import Router, Bot
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from handlers import check_date
from orm_top_messages import (orm_all_get_top_messages,
                              orm_get_messages_day, orm_get_messages_week,
                              orm_get_messages_custom)

top_msg = Router()


class AddDateMsg(StatesGroup):
    start_period = State()
    end_period = State()


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
async def get_all_top_messages(message: Message,
                               session: AsyncSession,
                               bot: Bot):

    total = await orm_all_get_top_messages(session)
    await output_text_message(total, message, bot)


@top_msg.message(F.text == "Статистика по сообщениям за день")
async def get_top_messages_day(message: Message,
                               session: AsyncSession,
                               bot: Bot):

    total = await orm_get_messages_day(session)
    await output_text_message(total, message, bot)


@top_msg.message(F.text == "Статистика сообщений по неделям")
async def get_top_messages_week(message: Message,
                                session: AsyncSession,
                                bot: Bot):
    total = await orm_get_messages_week(session)
    await output_text_message(total, message, bot)


@top_msg.message(StateFilter(None), F.text == 'Выбрать период по сообщениям')
async def get_message_add_start(message: Message, state: FSMContext):
    await message.answer(
        "Введи дату начала в формате год-месяц-день (например 2024-03-26)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddDateMsg.start_period)


@top_msg.message(AddDateMsg.start_period, F.text)
async def get_message_add_end(message: Message,
                              state: FSMContext,
                              ):
    if not await check_date(message):
        return
    await state.update_data(start_period=message.text)
    await message.answer(
        "Введи дату окончания(включительно) в формате год-месяц-день (например 2024-03-26)"
    )
    await state.set_state(AddDateMsg.end_period)


@top_msg.message(AddDateMsg.start_period)
async def check_start_msg(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


@top_msg.message(AddDateMsg.end_period, F.text)
async def finish_msg(message: Message,
                     state: FSMContext,
                     session: AsyncSession,
                     bot: Bot
                     ):
    if not await check_date(message):
        return
    await state.update_data(end_period=message.text)
    user_data = await state.get_data()
    print('USER_DATA', user_data)

    total = await orm_get_messages_custom(session,
                                          user_data.get('start_period'),
                                          user_data.get('end_period'))
    print('TOTAL', total)
    print('ЭТО СООБЩЕНИЯ ЗА ВЫБРАННЫЙ ПЕРИОД')
    await output_text_message(total, message, bot)

    await state.clear()


@top_msg.message(AddDateMsg.end_period)
async def check_finish_msg(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")
