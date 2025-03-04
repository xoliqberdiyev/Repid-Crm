from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.config import settings

engine = create_async_engine(
    url=settings.DB_URL,
    echo=True
)

async_session =  sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
