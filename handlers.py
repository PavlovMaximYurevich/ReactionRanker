import re
from typing import List

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import ADMIN_KEYBOARD
from orm_query import (orm_get_all_statistics,
                       orm_get_statistics_day,
                       orm_get_statistics_week,
                       orm_get_statistics_custom)

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


async def output_text(array: List, message: Message):
    if array:
        for user_data in array:
            user_data = list(user_data)
            for item in user_data:
                print(user_data)
                print(item)
                if item is None:
                    del item
        print(array)
        content = as_list(
            as_marked_section(
                Bold('Победители'),
                f'1 место по реакциям {array[0][0]} {array[0][1]}. Число реакции {array[0][2]}',
                # f'2 место по реакциям {array[1][0]}. Число реакции {array[1][1]}',
                marker="🏆 "
            )
        )
        await message.answer(
            **content.as_kwargs()
        )

    else:
        await message.answer("За выбранный период нет данных")


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу показать статистику\nНажми кнопку ниже",
        reply_markup=ADMIN_KEYBOARD,
    )


@router.message(F.text == 'Статистика за всё время')
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
