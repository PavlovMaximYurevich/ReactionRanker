from aiogram import Router
from aiogram import Bot
from aiogram.enums import ParseMode

from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, MessageReactionCountUpdated, MessageReactionUpdated
from aiogram.types.reaction_count import ReactionCount
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatMessages, Reactions
from handlers import text_message_sheduler
from orm_query import orm_add_message, orm_create_or_update_reactions

group_router = Router()


@group_router.message(Command("admin"))
async def get_admins(message: Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    #просмотреть все данные и свойства полученных объектов
    #print(admins_list)
    # Код ниже это генератор списка, как и этот x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    #print(admins_list)


@group_router.message()
async def message_handler(message: Message, session: AsyncSession):
    # Получить chat_id
    # print(message)
    # if message.chat.id == '-1001512201546':
    await orm_add_message(session, message)
    # print(message)


@group_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated,
                                   session: AsyncSession,
                                   ):
    # if message_reaction.chat.id == '-1001512201546':
    await orm_create_or_update_reactions(session,
                                         message_reaction,
                                         message_id=message_reaction.message_id)


