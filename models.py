import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST, TYPE_DB


PG_DSN = f'{TYPE_DB}+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
