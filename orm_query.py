from aiogram.types import Message, MessageReactionUpdated, ReactionCount, MessageReactionCountUpdated
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatMessages, Reactions


async def orm_add_message(session: AsyncSession, message: Message):
    session.add(ChatMessages(
        id_message=message.message_id,
        text=message.text,
        created_date=message.date,
        username=f'@{message.from_user.username}',
        id_username=message.from_user.id
    ))
    await session.commit()


async def orm_create_or_update_reactions(session: AsyncSession,
                                         message_reaction: MessageReactionUpdated,
                                         message_id: int,
                                         ):
    sql = select(Reactions.count_reactions).where(Reactions.id_message == message_id)

    result = await session.execute(sql)
    # print('RESULT', result.fetchall())

    if result.fetchall():
        print("UPDATE")
        # print('RESULT', result.fetchall())
        # qqq = select(Reactions.reactions).where(Reactions.id_message == message_id)
        sql_select = select(Reactions.count_reactions).where(Reactions.id_message == message_id)
        reactions = await session.execute(sql_select)
        list_reactions = reactions.fetchall()  # реакции из БД
        print('COUNT_REACTIONS', list_reactions)
        flag = len(message_reaction.new_reaction) - len(message_reaction.old_reaction)

        # flag = 1
        # count_list_msg.pop()
        # print('AFTER_POP', count_list_msg)
        # if len(count_list_msg) == 1:
        #     flag = 1
        # else:
        #     flag = -1

        query = update(Reactions).where(Reactions.id_message == message_id).values(
            id_message=message_reaction.message_id,
            reactions=str(message_reaction.new_reaction),
            count_reactions=list_reactions[0][0] + flag
        )
        await session.execute(query)
        await session.commit()

    else:
        print('CREATE')

        session.add(Reactions(
            id_message=message_reaction.message_id,
            # count_reactions=len(message_reaction.new_reaction)
            # reactions=emoji.emoji,
            reactions=str(message_reaction.new_reaction),
            count_reactions=len(message_reaction.new_reaction)
            # count_reactions=len(result.fetchall())
        ))
        await session.commit()
        # else:
        #     del message_reaction.new_reaction[-1]
        #     print('CREATE DEL', message_reaction.new_reaction)

# async def orm_update_reactions(session: AsyncSession,
#                                message_reaction: MessageReactionUpdated,
#                                message_id: int):
#     q = select(Reactions).where(Reactions.id_message == message_id)
#     result = await session.execute(q)
#     if result.scalars().all():
#         print('AAAAAAAAAA')
#
#     query = update(Reactions).where(Reactions.id_message == message_id).values(
#         id_message=message_reaction.message_id,
#         count_reactions=len(message_reaction.new_reaction)
#     )
#     await session.execute(query)
#     await session.commit()
