from aiogram import Router
from aiogram import Bot
from aiogram.enums import ParseMode

from aiogram.filters import CommandStart, StateFilter
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


@group_router.message()
async def message_handler(message: Message, session: AsyncSession):
    # Получить chat_id
    print(message)
    await orm_add_message(session, message)
    # print(message)


@group_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated,
                                   session: AsyncSession,
                                   ):
    await orm_create_or_update_reactions(session,
                                         message_reaction,
                                         message_id=message_reaction.message_id)


