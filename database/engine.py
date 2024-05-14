import os

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)

from database.models import Base


# engine = create_async_engine('postgresql+asyncpg://ofjoptkv:iNw-pmVdF7rJvn3z0Wo57jMZo3QtPDbI@hattie.db.elephantsql.com/ofjoptkv', echo=True)
engine = create_async_engine('sqlite+aiosqlite:///sqlite.db', echo=True)

session_maker = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def create_db():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
