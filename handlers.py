import re
from typing import List

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import ADMIN_KEYBOARD

from orm_query import (orm_get_all_statistics,
                       orm_get_statistics_day,
                       orm_get_statistics_week,
                       orm_get_statistics_custom)
from orm_top_messages import orm_all_get_top_messages

router = Router()


class AddDate(StatesGroup):
    start_period = State()
    end_period = State()


async def check_date(message: Message):
    r = re.search(r'\b\d{4}-\d{2}-\d{2}\b', message.text)
    if not r:
        await message.answer(
            "Введён неверный формат даты, введите еще раз"
        )
        return False
    return True


async def truncate_last_name(first_name: str,
                             last_name: str,
                             ) -> str:
    if last_name is None:
        return f'{first_name}'
    else:
        return f'{first_name} {last_name}'


async def text_message_sheduler(array: List) -> str:
    if array:
        ind = 1
        msg = '⭐️ Друзья, хочу поблагодарить самых активных и полезных участников нашего сообщества на этой неделе:\n'
        max_user = 10
        if len(array) > max_user:
            array = array[:max_user]
        for id_user, name, surname, count_reactions in array:
            if ind == 1:
                link = f'🥇 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            elif ind == 2:
                link = f'🥈 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            elif ind == 3:
                link = f'🥉 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            else:
                link = f' {ind}.  <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            ind += 1
        return msg
    return "За выбранный период нет данных"


async def output_text(array: List, message: Message):
    if array:
        ind = 1
        msg = ''
        max_user = 10
        if len(array) > max_user:
            array = array[:max_user]
        for id_user, name, surname, count_reactions in array:
            if ind == 1:
                link = f'🥇 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            elif ind == 2:
                link = f'🥈 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            elif ind == 3:
                link = f'🥉 <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            else:
                link = f'{ind}.  <a href="tg://user?id={id_user}">{await truncate_last_name(name, surname)}</a>'
                msg += f'{link} - {count_reactions}\n'
            ind += 1

        await message.answer(
            f'Топ юзеров: \n{msg}',
            parse_mode=ParseMode.HTML
        )

    else:
        await message.answer("За выбранный период нет данных")


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу показать статистику\nНажми кнопку ниже",
        reply_markup=ADMIN_KEYBOARD,
    )


# @router.message(F.text =='Статистика по сообщениям за всё время')
# async def message_statistics(message: Message):
#     await message.answer(
#         text="Выбери",
#         reply_markup=MESSAGES_KB,
#     )


@router.message(F.text == 'Статистика по реакциям за всё время')
async def get_all_statistics(message: Message, session: AsyncSession):
    total = await orm_get_all_statistics(session)
    # print(total)
    print('ЭТО ВСЕ РЕАКЦИИ')
    await output_text(total, message)


@router.message(F.text == 'За день')
async def get_statistics_day(message: Message, session: AsyncSession):
    total = await orm_get_statistics_day(session)
    await output_text(total, message)


@router.message(F.text == 'За неделю')
async def get_statistics_week(message: Message, session: AsyncSession):
    total = await orm_get_statistics_week(session)
    print('ЭТО РЕАКЦИИ ЗА НЕДЕЛЮ')
    await output_text(total, message)


@router.message(StateFilter(None), F.text == 'Выбрать период')
async def get_statistics_add_start(message: Message, state: FSMContext):
    await message.answer(
        "Введи дату начала в формате год-месяц-день (например 2024-03-26)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddDate.start_period)


@router.message(AddDate.start_period, F.text)
async def get_statistics_add_end(message: Message,
                                 state: FSMContext,
                                 ):
    if not await check_date(message):
        return
    await state.update_data(start_period=message.text)
    await message.answer(
        "Введи дату окончания(включительно) в формате год-месяц-день (например 2024-03-26)"
    )
    await state.set_state(AddDate.end_period)


@router.message(AddDate.start_period)
async def check_start(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


@router.message(AddDate.end_period, F.text)
async def finish(message: Message,
                 state: FSMContext,
                 session: AsyncSession
                 ):
    if not await check_date(message):
        return
    await state.update_data(end_period=message.text)
    user_data = await state.get_data()
    print('USER_DATA', user_data)

    total = await orm_get_statistics_custom(session,
                                            user_data.get('start_period'),
                                            user_data.get('end_period'))
    print('ЭТО РЕАКЦИИ ЗА ВЫБРАННЫЙ ПЕРИОД')
    await output_text(total, message)

    await state.clear()


@router.message(AddDate.end_period)
async def check_finish(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


# @router.message(F.text == "Статистика по сообщениям за всё время")
# async def get_all_top_messages(message: Message, session: AsyncSession):
#     total = await orm_all_get_top_messages(session)
#     print(total)
#     print('ЭТО ВСЕ СООБЩЕНИЯ')
#     # await output_text(total, message)
#     # print(total[0][0])
#     await bot.send_message(chat_id='-1002084425436', text='Тест', reply_to_message_id=total[0][0])
