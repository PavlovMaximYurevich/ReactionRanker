import re

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


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу показать статистику\nНажми кнопку ниже",
        reply_markup=ADMIN_KEYBOARD,
    )


@router.message(F.text == 'Статистика за всё время')
async def get_all_statistics(message: Message, session: AsyncSession):
    total = await orm_get_all_statistics(session)
    print('ЭТО ВСЕ РЕАКЦИИ')
    if total:
        await message.answer(
            f'1 место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
            f'2 место по реакциям {total[1][0]}. Число реакции {total[1][1]}'
        )
    else:
        await message.answer("За выбранный период нет данных")


@router.message(F.text == 'За день')
async def get_statistics_day(message: Message, session: AsyncSession):
    total = await orm_get_statistics_day(session)
    print('ЭТО РЕАКЦИИ ЗА ДЕНЬ')
    if total:
        await message.answer(
            f'1 место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
            f'2 место по реакциям {total[1][0]}. Число реакции {total[1][1]}'
        )
    else:
        await message.answer("За выбранный период нет данных")


@router.message(F.text == 'За неделю')
async def get_statistics_week(message: Message, session: AsyncSession):
    total = await orm_get_statistics_week(session)
    print('ЭТО РЕАКЦИИ ЗА НЕДЕЛЮ')
    if total:
        await message.answer(
            f'1 место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
            f'2 место по реакциям {total[1][0]}. Число реакции {total[1][1]}',
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer("За выбранный период нет данных")


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
    # r = re.search(r'\b\d{4}-\d{2}-\d{2}\b', message.text)
    # if not r:
    #     await message.answer(
    #         "Введён неверный формат даты, введите еще раз"
    #     )
    #     return
    if not await check_date(message):
        return
    await state.update_data(start_period=message.text)
    await message.answer("Введи дату окончания(включительно) в формате год-месяц-день (например 2024-03-26)")
    await state.set_state(AddDate.end_period)


@router.message(AddDate.start_period)
async def check_start(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


@router.message(AddDate.end_period, F.text)
async def finish(message: Message,
                 state: FSMContext,
                 session: AsyncSession
                 ):
    r = re.search(r'\b\d{4}-\d{2}-\d{2}\b', message.text)
    # if not r:
    #     await message.answer(
    #         "Введён неверный формат даты, введите еще раз"
    #     )
    #     return
    if not await check_date(message):
        return
    await state.update_data(end_period=message.text)
    user_data = await state.get_data()
    print('USER_DATA', user_data)

    total = await orm_get_statistics_custom(session,
                                            user_data.get('start_period'),
                                            user_data.get('end_period'))
    print('ЭТО РЕАКЦИИ ЗА ВЫБРАННЫЙ ПЕРИОД')
    if total:
        await message.answer(
            f'1 место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
            f'2 место по реакциям {total[1][0]}. Число реакции {total[1][1]}',
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer("За выбранный период нет данных")

    await state.clear()


@router.message(AddDate.end_period)
async def check_finish(message: Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")
