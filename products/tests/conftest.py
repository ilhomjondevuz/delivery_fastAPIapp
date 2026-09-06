import pytest
from environs import Env

from accounts.models import User
from database import Base

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


env = Env()
env.read_env()

TEST_DATABASE_URL = env.str("TEST_DATABASE_URL")

engine = create_async_engine(
    TEST_DATABASE_URL
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def user(db):
    user = User(
        username="test_user",
        email="test_email@gmail.com",
        password="qwerty123!",
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user