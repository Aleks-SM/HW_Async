import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON, String
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST, TYPE_DB

# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
# POSTGRES_USER = os.getenv('POSTGRES_USER', 'swapi')
# POSTGRES_DB = os.getenv('POSTGRES_DB', 'swapi')
# POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
# POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'{TYPE_DB}+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    gender: Mapped[str] = mapped_column(String(10))
    birth_year: Mapped[str] = mapped_column(String(10))
    eye_color: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(20))
    skin_color: Mapped[str] = mapped_column(String(20))
    height: Mapped[str] = mapped_column(String(50))
    mass: Mapped[str] = mapped_column(String(10))
    homeword: Mapped[str] = mapped_column(String(30))
    films: Mapped[str] = mapped_column(String(150))
    species: Mapped[str] = mapped_column(String(150))
    starships: Mapped[str] = mapped_column(String(150))
    vehicles: Mapped[str] = mapped_column(String(150))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
