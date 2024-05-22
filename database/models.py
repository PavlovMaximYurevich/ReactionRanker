# from datetime import datetime
import datetime

from sqlalchemy import Text, DateTime, Integer, String, func, ForeignKey, LargeBinary
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class ChatMessages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_message: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(150), nullable=False)
    # message: Mapped[JSON] = mapped_column(JSON, nullable=False)
    created_date: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    id_username: Mapped[int] = mapped_column(Integer, nullable=False)


class Reactions(Base):
    __tablename__ = 'reactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_message: Mapped[int] = mapped_column(ForeignKey('messages.id_message'), nullable=False)
    count_reactions: Mapped[int] = mapped_column(Integer)
