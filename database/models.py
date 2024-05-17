# from datetime import datetime
import datetime

from sqlalchemy import Text, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class ChatMessages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_message: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_date: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    id_username: Mapped[int] = mapped_column(Integer, nullable=False)


class Reactions(Base):
    __tablename__ = 'reactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_message: Mapped[int] = mapped_column(ForeignKey('messages.id_message'), nullable=False)
    reactions: Mapped[str] = mapped_column(Text)
    count_reactions: Mapped[int] = mapped_column(Integer)
