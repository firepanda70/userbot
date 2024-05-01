from sqlalchemy import MetaData
from sqlalchemy.orm import (
    declared_attr, DeclarativeBase, sessionmaker
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .settings import get_config

config = get_config()

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

class BaseDBModel(DeclarativeBase):
    metadata = MetaData(
        naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION
    )
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


engine = create_async_engine(f'postgresql+asyncpg://{config.db_url}')
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession)
