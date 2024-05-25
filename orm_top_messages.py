from datetime import timedelta, date

from aiogram.types import Message, MessageReactionUpdated
from sqlalchemy import update, select, func, Date, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatMessages, Reactions


async def orm_all_get_top_messages(session: AsyncSession):
    """Статистика по сообщениям за всё время."""

    queryset = select(
        ChatMessages.id_message,
        ChatMessages.content_type,
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.max(Reactions.count_reactions).label("count")
    ).join(
        Reactions,
        ChatMessages.id_message == Reactions.id_message
    ).group_by(
        ChatMessages.id_message
        # ChatMessages.username, ChatMessages.last_name
    ).order_by(desc('count')).limit(10)

    res = await session.execute(queryset)

    # print('RES_FIRST', res.first())
    return res.first()


async def orm_get_messages_day(session: AsyncSession):
    """Статистика сообщений по дням."""

    queryset = select(
        ChatMessages.id_message,
        ChatMessages.content_type,
        ChatMessages.id_username,
        ChatMessages.name,
        ChatMessages.last_name,
        func.max(Reactions.count_reactions).label("count")
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

