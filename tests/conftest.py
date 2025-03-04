import asyncio
import os
from datetime import timedelta
from datetime import datetime
from typing import List
from sqlalchemy import select, insert

from database import models
import asyncpg
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from sqlalchemy import text

from database.session import get_db
from main import app
from utils import security, settings, hashing

import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


CLEAN_TABLES = [
    "positions",
    "employees"
]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.DATABASE_URL_TEST, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))

async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            settings.DATABASE_URL_TEST, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass

@pytest.fixture(scope="function")
async def client():
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.DATABASE_URL_TEST.split("+asyncpg"))
    )
    yield pool
    pool.close()

@pytest.fixture
async def create_position_from_database(async_session_test):
    async def create_position_from_database(name):
        async with async_session_test() as session:
            async with session.begin():
                position = await session.execute(insert(models.Position).values(name=name).returning(models.Position.id))
                await session.commit()
                position_id = position.scalar_one()  # Fetch the id
                return position_id
    return create_position_from_database


@pytest.fixture
async def get_user_from_database(async_session_test):
    async def get_user_from_database_by_uuid():
        async with async_session_test() as session:
            async with session.begin():
                data = await session.execute(select(models.Position))
                return data.scalar_one()
    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(async_session_test:AsyncSession):
    async def _create_user_in_database(
        username: str,
        last_name: str,
        first_name: str,
        phone_number: str,
        salary: int,
        position_id: int,
        password: str,
        user_type: str,
        is_active: bool,
        date_of_birth: datetime,
        date_of_jobstarted: datetime,
        created_time: datetime,
    ):
        async with async_session_test() as session:
            async with session.begin():
                data = await session.execute(insert(models.Employees).values(
                    username=username,
                        last_name=last_name,
                        first_name=first_name,
                        phone_number=phone_number,
                        salary=salary,
                        position_id=position_id,
                        password=hashing.Hasher.get_password_hash(password),
                        user_type=user_type,
                        is_active=is_active,
                        date_of_birth=date_of_birth,
                        date_of_jobstarted=date_of_jobstarted,
                        created_time=created_time
                ).returning(models.Employees.id))
                await session.commit()
            return data.scalar_one()
    return _create_user_in_database

@pytest.fixture
async def create_project_in_database(async_session_test):
    async def create_project_in_database(
            name:str,
            start_date:datetime,
            end_date:datetime,
            price:str,
            progemmer_list:List[str]
            ):
        async with async_session_test() as session:
            async with session.begin():
                project = await session.execute(insert(models.Project).values(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    price=price,
                    image='nano'
                ).returning(models.Project))

                project_ = project.scalar_one()

                for programer_id in progemmer_list:
                    await session.execute(insert(models.ProjectProgrammer).values(
                                project_id=project_.id,
                                programmer_id = int(programer_id)
                            ))
                
                await session.commit()
        return project_
    return create_project_in_database

@pytest.fixture
async def create_expense_in_database(async_session_test):
    async def _create_expense_in_database(name:str,
                                          description:str,
                                          from_whom:str,
                                          date_paied:datetime,
                                          price_paid:str,
                                          type:str):
        async with async_session_test() as session:
            async with session.begin():
                data_expense = await session.execute(insert(models.ExpenseData).values(
                    name=name,
                    description=description,
                    from_whom = from_whom,
                    date_paied=date_paied,
                    price_paid=price_paid,
                    type=type
                ).returning(models.ExpenseData))
                await session.commit()
            return data_expense.scalar_one()
        
    return _create_expense_in_database
    
    


def create_test_auth_headers_for_user(username: str) -> dict[str, str]:
    access_token = security.create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"Authorization": f"Bearer {access_token}"}




