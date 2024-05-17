from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import ADMIN_KEYBOARD
from orm_query import orm_get_all_statistics, orm_get_statistics_day

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу показать статистику\nНажми кнопку ниже",
        reply_markup=ADMIN_KEYBOARD,
    )


@router.message(F.text == 'Статистика')
async def get_all_statistics(message: Message, session: AsyncSession):
    total = await orm_get_all_statistics(session)
    print('ЭТО ВСЕ РЕАКЦИИ')
    await message.answer(f'Первое место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
                         f'Второе место по реакциям {total[1][0]}. Число реакции {total[1][1]}')


@router.message(F.text == 'За день')
async def get_statistics_day(message: Message, session: AsyncSession):
    total = await orm_get_statistics_day(session)
    print('ЭТО РЕАКЦИИ ЗА ДЕНЬ')
    await message.answer(f'Первое место по реакциям {total[0][0]}. Число реакции {total[0][1]}\n'
                         f'Второе место по реакциям {total[1][0]}. Число реакции {total[1][1]}')

