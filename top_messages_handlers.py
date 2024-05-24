from aiogram import Router
# from aiogram import F
# from aiogram.types import Message
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# from orm_top_messages import orm_all_get_top_messages
#
# #
# top_msg = Router()
#
#
# @top_msg.message(F.text == "Статистика по сообщениям")
# async def get_all_top_messages(message: Message, session: AsyncSession):
#     total = await orm_all_get_top_messages(session)
#     print(total)
#     print('ЭТО ВСЕ СООБЩЕНИЯ')
#     # await output_text(total, message)
#     await message.answer("Вот статистика по сообщениям")
