from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

env = Env()
env.read_env()

# mysql + package_name://user:password@host/database
DATABASE_URL = env.str('DATABASE_URL')

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

Session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)