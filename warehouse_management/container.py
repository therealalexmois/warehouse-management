from dependency_injector import containers, providers

from warehouse_management.infrastructure.database import SessionFactory
from warehouse_management.infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository
from warehouse_management.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from warehouse_management.settings import settings


class AppContainer(containers.DeclarativeContainer):
    """Контейнер инъекции зависимостей"""

    config = providers.Singleton(lambda: settings)

    session = providers.Singleton(SessionFactory)

    product_repository = providers.Singleton(SqlAlchemyProductRepository, session=session)
    order_repository = providers.Singleton(SqlAlchemyOrderRepository, session=session)

    unit_of_work = providers.Singleton(SqlAlchemyUnitOfWork, session=session)
