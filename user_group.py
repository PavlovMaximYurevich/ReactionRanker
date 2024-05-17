from aiogram import Router
from aiogram import Bot

from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, MessageReactionCountUpdated, MessageReactionUpdated
from aiogram.types.reaction_count import ReactionCount
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatMessages, Reactions
from orm_query import orm_add_message, orm_create_or_update_reactions

group_router = Router()


async def current_list(list_reactions: list) -> int:
    return len(list_reactions)


@group_router.message()
async def message_handler(message: Message, session: AsyncSession):
    # Получить chat_id
    await orm_add_message(session, message)
    print(message.text)


@group_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated,
                                   session: AsyncSession,
                                   ):
    await orm_create_or_update_reactions(session,
                                         message_reaction,
                                         message_id=message_reaction.message_id)
