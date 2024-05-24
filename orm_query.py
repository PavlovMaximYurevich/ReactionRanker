from datetime import timedelta, date

from aiogram.types import Message, MessageReactionUpdated
from sqlalchemy import update, select, func, Date, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatMessages, Reactions


async def orm_add_message(session: AsyncSession, message: Message):

    session.add(ChatMessages(
        id_message=message.message_id,
        content_type=message.content_type,
        created_date=message.date + timedelta(hours=3),
        username=message.from_user.username,
        name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        id_username=message.from_user.id
    ))
    await session.commit()


async def orm_create_or_update_reactions(session: AsyncSession,
                                         message_reaction: MessageReactionUpdated,
                                         message_id: int,
                                         ):
    sql = select(Reactions.count_reactions).where(Reactions.id_message == message_id)

    result = await session.execute(sql)

    if result.fetchall():
        print("UPDATE")

        sql_select = select(Reactions.count_reactions).where(Reactions.id_message == message_id)
        reactions = await session.execute(sql_select)
        list_reactions = reactions.fetchall()  # реакции из БД
        print('COUNT_REACTIONS', list_reactions)
        negative_emoji_new = 0
        negative_emoji_old = 0
        for emoji in message_reaction.new_reaction:
            if emoji.emoji in ['💩', '👎', '🤬', '😡']:
                negative_emoji_new += 1
        for emoji in message_reaction.old_reaction:
            if emoji.emoji in ['💩', '👎', '🤬', '😡']:
                negative_emoji_old += 1
        new_reactions = len(message_reaction.new_reaction)
        old_reactions = len(message_reaction.old_reaction)
        # flag = len(message_reaction.new_reaction) - len(message_reaction.old_reaction)
        flag = (new_reactions - negative_emoji_new) - (old_reactions - negative_emoji_old)

        query = update(Reactions).where(Reactions.id_message == message_id).values(
            id_message=message_reaction.message_id,
            count_reactions=list_reactions[0][0] + flag
        )
        await session.execute(query)
        await session.commit()

    else:
        print('CREATE')

        session.add(Reactions(
            id_message=message_reaction.message_id,
            count_reactions=len(message_reaction.new_reaction)
        ))
        await session.commit()


async def orm_get_all_statistics(session: AsyncSession):
    """Статистика за всё время."""

    queryset = select(
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.sum(Reactions.count_reactions).label("count")
    ).join(
        Reactions,
        ChatMessages.id_message == Reactions.id_message
    ).group_by(
        ChatMessages.username, ChatMessages.last_name
    ).order_by(desc('count'))

    res = await session.execute(queryset)

    # print(res.all())
    return res.all()


async def orm_get_statistics_day(session: AsyncSession):
    """Статистика по дням."""

    queryset = select(
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.sum(Reactions.count_reactions).label("count")
    ).join(
        Reactions,
        ChatMessages.id_message == Reactions.id_message
    ).where(
        func.date(ChatMessages.created_date) == date.today()
    ).group_by(
        ChatMessages.username, ChatMessages.last_name
    ).order_by(desc('count'))

    res = await session.execute(queryset)

    # print('RES_ALL', res.all())
    return res.all()


async def orm_get_statistics_week(session: AsyncSession):
    """Статистика по неделям."""

    queryset = select(
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.sum(Reactions.count_reactions).label("count")
    ).join(
        Reactions,
        ChatMessages.id_message == Reactions.id_message
    ).where(
        func.date(ChatMessages.created_date) >= date.today() - timedelta(days=6)
    ).group_by(
        ChatMessages.username, ChatMessages.last_name
    ).order_by(desc('count'))

    res = await session.execute(queryset)

    # print('RES_ALL', res.all())
    return res.all()


async def orm_get_statistics_custom(session: AsyncSession,
                                    start_period: Date,
                                    end_period: Date):
    """Статистика по выбранному периоду."""

    queryset = select(
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.sum(Reactions.count_reactions).label("count")
    ).join(
        Reactions, ChatMessages.id_message == Reactions.id_message
    ).where(
        func.date(ChatMessages.created_date).between(start_period, end_period)
    ).group_by(
        ChatMessages.username, ChatMessages.last_name
    ).order_by(desc('count'))

    res = await session.execute(queryset)

    # print('RES_ALL', res.all())
    return res.all()
