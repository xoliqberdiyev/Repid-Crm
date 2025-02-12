from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from utils import settings


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)

engine_test = create_async_engine(
    url=settings.DATABASE_URL_TEST,
    echo=True
)

async_session =  async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async_session_test = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()

async def get_db_test():
    try:
        session:AsyncSession = async_session()
        yield session
    finally:
        await session.close()