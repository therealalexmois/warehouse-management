"""Модуль для инициализации базы данных и управления соединением."""

from typing import TYPE_CHECKING

from dependency_injector.wiring import inject, Provide
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from warehouse_management.container import AppContainer
from warehouse_management.infrastructure.orm import Base

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


@inject
def get_engine(database_url: str = Provide[AppContainer.config.database.url]) -> 'Engine':
    """Создает движок базы данных с использованием зависимости из контейнера.

    Args:
        database_url (str): URL базы данных, полученный из DI-контейнера.

    Returns:
        Engine: Экземпляр SQLAlchemy Engine.
    """
    return create_engine(database_url)


engine = get_engine()

SessionFactory = sessionmaker(bind=engine)


def init_db() -> None:
    """Инициализирует базу данных, создавая таблицы, если они отсутствуют."""
    Base.metadata.create_all(engine)
