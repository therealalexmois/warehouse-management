import os
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from warehouse_management.infrastructure.orm import Base
from warehouse_management.infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository
from warehouse_management.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.engine import Engine


@pytest.fixture(scope='session')
def in_memory_db() -> 'Generator[Engine]':
    """Создает базу данных в памяти (SQLite) для unit-тестов."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(in_memory_db: 'Engine') -> 'Generator[Session]':
    """Создает новую сессию базы данных для теста."""
    connection = in_memory_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def product_repo(db_session: 'Session') -> 'SqlAlchemyProductRepository':
    """Создает тестовый репозиторий товаров."""
    return SqlAlchemyProductRepository(db_session)


@pytest.fixture
def order_repo(db_session: 'Session') -> 'SqlAlchemyOrderRepository':
    """Создает тестовый репозиторий заказов."""
    return SqlAlchemyOrderRepository(db_session)


@pytest.fixture
def unit_of_work(db_session: 'Session') -> 'SqlAlchemyUnitOfWork':
    """Создает тестовый Unit of Work."""
    return SqlAlchemyUnitOfWork(db_session)


@pytest.fixture(scope='session')
def docker_compose_file(pytestconfig) -> str:  # noqa: ANN001
    """Указывает путь к `docker-compose.yml` для `pytest-docker`."""
    return os.path.join(str(pytestconfig.rootdir), 'tests', 'docker', 'docker-compose.yml')
