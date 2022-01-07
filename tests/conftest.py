import pytest
from httpx import AsyncClient

from main import app
from settings import get_settings


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver.com") as client:
        yield client


import os
from urllib.parse import urlparse

import psycopg2
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import alembic.config

settings = get_settings()
parsed_db_uri = urlparse(settings.POSTGRES_TEST_URL)
print(parsed_db_uri)
db = parsed_db_uri.path.lstrip("/")


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    conn = psycopg2.connect(
        f"host={parsed_db_uri.hostname} user={parsed_db_uri.username} password={parsed_db_uri.password}"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db}")
    cur.execute(f"CREATE DATABASE {db}")
    alembic.config.main(argv=["-c", "./alembic.ini", "upgrade", "head"])
    yield
    # cur.execute("DROP DATABASE test_auth") leave the database up after the test.  will tear it down for next test anyway.


@pytest.mark.asyncio
@pytest.fixture
async def session():
    engine = create_async_engine(
        os.environ["POSTGRES_TEST_URL"], future=True, echo=True
    )
    conn = await engine.connect()
    print("fixture begin Nested >>>>>>")
    transaction = await conn.begin_nested()
    session = sessionmaker(
        bind=conn, class_=AsyncSession, expire_on_commit=False, future=True
    )
    async with session() as db_session:
        yield db_session
        print("<<<<<<<< fixture rollback")
        await transaction.rollback()
        await conn.close()
        await engine.dispose()
