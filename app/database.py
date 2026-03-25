from typing import Annotated, Optional

from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy import URL, text, String
from sqlalchemy.testing.schema import mapped_column

from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

engin = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

session = sessionmaker(engin)


class Base(DeclarativeBase):

    # Определяем композируемые типы
    @classmethod
    def _str_field(cls, length: int = 256, **kwargs):
        """Базовый метод для создания строковых полей"""
        return Annotated[str, mapped_column(String(length), **kwargs)]

    @staticmethod
    def str_field_nullable(length: int = 256, **kwargs):
        """Создает nullable Annotated строковое поле"""
        return Annotated[
            Optional[str], mapped_column(String(length), **kwargs)]

    # Публичные типы
    str_256 = _str_field(256)
    str_256_indexed = _str_field(256, index=True)

    # Nullable версии
    str_256_nullable = str_field_nullable(256)
    str_256_indexed_nullable = str_field_nullable(256, index=True)

    # Стандартные системные поля
    id = Annotated[int, mapped_column(primary_rey=True)]
