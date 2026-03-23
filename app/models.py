from sqlalchemy import String, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Source(Base):
    """Источник материала: загруженный файл или найденная книга"""
    __tablename__ = 'source'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256), index=True)
    author: Mapped[Optional[str]] = mapped_column(String(256), index=True)

    # Тип контента: 'file', 'book_name', 'youtube_url'
    source_type: Mapped[str] = mapped_column(String(50))

    # Путь к файлу (если загружен) или описание для поиска
    content_path: Mapped[str] = mapped_column(Text)

    test: Mapped[List["Test"]] = relationship(back_populates='source',
                                              cascade='all, delete-orphan')
    # Время создания
    created_at: Mapped[DateTime] = mapped_column(default=datetime.utcnow)


class Test(Base):
    """Сам тест, созданный нейронкой"""
    __tablename__ = 'test'

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey('source.id'))

    # Уровень сложности или тема (например, "Глава 1")
    metadata_info: Mapped[Optional[str]] = mapped_column(String(100))

    source: Mapped["Source"] = relationship(back_populates="tests")
    questions: Mapped[List["Question"]] = relationship(back_populates="test",
                                                       cascade="all, delete-orphan")


class Question(Base):
    """Конкретный вопрос теста"""
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey('test.id'))

    question_text: Mapped[str] = mapped_column(Text)

    # Варианты ответов храним в JSON: {"A": "текст", "B": "текст"...}
    options: Mapped[dict] = mapped_column(JSON)

    # Правильный ответ (ключ из JSON)
    correct_answer: Mapped[str] = mapped_column(String(10))

    # Объяснение от нейронки, почему этот ответ верный
    explanation: Mapped[Optional[str]] = mapped_column(Text)

    test: Mapped['Test'] = relationship(back_populates='question')
