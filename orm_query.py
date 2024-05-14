from aiogram.types import Message, MessageReactionUpdated, ReactionCount
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
    # qqq = select(Reactions)
    # res = await session.execute(qqq)
    # print(res.scalars().all())

    q = select(Reactions.reactions).where(Reactions.id_message == message_id)

    result = await session.execute(q)
    # print('RESULT', result.fetchall())

    if result.fetchall():
        print("UPDATE")
        # print('RESULT', result.fetchall())
        qqq = select(Reactions.reactions).where(Reactions.id_message == message_id)
        r = await session.execute(qqq)
        # print('RSCALARS', r.scalars().all())
        # print('ДЛИНА', len(r.fetchall()))

        # for emoji in message_reaction.new_reaction:
        #     if emoji.emoji not in ['💩', '👎', '🤬', '😡']:
        #         print('UPDATE', message_reaction.new_reaction)
        # a = await session.scalars(select(Reactions).where(Reactions.id_message == message_id))
        # print(a.all())
        # for i in a.all():
        #     print(i.)
        # print('REACTIONS', await session.execute(select(Reactions).where(Reactions.id_message == message_id)))
        # qqq = select(Reactions.reactions).where(Reactions.id_message == message_id)
        # r = await session.execute(qqq)

        query = update(Reactions).where(Reactions.id_message == message_id).values(
            id_message=message_reaction.message_id,
            # reactions=emoji.emoji,
            reactions=str(message_reaction.new_reaction),
            count_reactions=len(r.fetchall())
        )

        await session.execute(query)
        await session.commit()
        # print('FETCHALL', r.fetchall())
        # print('ДЛИНА', len(r.fetchall()))
        # print('Длина списка', reactions.count_reactions)
            # else:
            #     del message_reaction.new_reaction[-1]
            #     print('UPDATE DEL', message_reaction.new_reaction)
    else:
        print('CREATE')
        # for emoji in message_reaction.new_reaction:
            # if emoji.emoji not in ['💩', '👎', '🤬', '😡']:
        #         print('CREATE', message_reaction.new_reaction)
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
