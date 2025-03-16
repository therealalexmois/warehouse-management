"""Модуль контейнера зависимостей для управления зависимостями приложения.

Этот модуль использует `dependency_injector`, чтобы управлять созданием и передачей зависимостей
в различных частях приложения.
"""

from dependency_injector import containers, providers

from warehouse_management.infrastructure.database import SessionFactory
from warehouse_management.infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository
from warehouse_management.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


class AppContainer(containers.DeclarativeContainer):
    """Контейнер инъекции зависимостей для управления компонентами приложения.

    Этот контейнер управляет созданием сессий БД, репозиториев и Unit of Work.
    """

    config = providers.Configuration()

    session = providers.Singleton(SessionFactory)

    product_repository = providers.Singleton(SqlAlchemyProductRepository, session=session)
    order_repository = providers.Singleton(SqlAlchemyOrderRepository, session=session)

    unit_of_work: providers.Singleton[SqlAlchemyUnitOfWork] = providers.Singleton(SqlAlchemyUnitOfWork, session=session)
