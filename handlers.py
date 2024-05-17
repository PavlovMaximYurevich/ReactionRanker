from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, MessageReactionCountUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import get_keyboard
from orm_query import orm_get_all_statistics

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу показать статистику\nНажми кнопку ниже",
        reply_markup=get_keyboard(
            "Статистика",
            # "Все мероприятия",
            placeholder="Статистика",
            sizes=(2,)
        ),
    )


@router.message(F.text == 'Статистика')
async def get_all_events(message: Message, session: AsyncSession):
    # total_list = []
    for item in await orm_get_all_statistics(session):
        print(item)
    total = await orm_get_all_statistics(session)
    # print(total_list)
    await message.answer(f'Первое место по реакциям {total[-1][0]}. Число реакции {total[-1][1]}\n'
                         f'Второе место по реакциям {total[-2][0]}. Число реакции {total[-2][1]}')





# @router.message()
# async def echo(message: Message):
#     print(message)
#     await message.answer('AAA')
