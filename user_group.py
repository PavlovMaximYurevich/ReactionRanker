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


# async def list_reactions(message_reaction: MessageReactionUpdated):
#     return message_reaction.new_reaction


@group_router.message()
async def message_handler(message: Message, session: AsyncSession):

    await orm_add_message(session, message)
    print(message.text)


@group_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated,
                                   session: AsyncSession,
                                   ):
    # for emoji in message_reaction.new_reaction:
    #     if emoji.emoji not in ['💩', '👎', '🤬', '😡']:
    await orm_create_or_update_reactions(session,
                                         message_reaction,
                                         message_id=message_reaction.message_id)


# @group_router.message_reaction_count()
# async def msg_reactions_count(msg: MessageReactionCountUpdated, react: MessageReactionUpdated):
#     print(react.new_reaction)
    # print(msg.message_id)

#
# @group_router.message_reaction_count()
# async def message_reaction_handler(message_reaction: ReactionCount,
#                                    session: AsyncSession,
#                                    ):
#     print('CDYTIIIIIIIIIIIIIII', message_reaction.total_count)
