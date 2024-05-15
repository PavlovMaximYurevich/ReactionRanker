from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, MessageReactionCountUpdated


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я бот"
    )





# @router.message()
# async def echo(message: Message):
#     print(message)
#     await message.answer('AAA')
