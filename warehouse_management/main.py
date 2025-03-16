"""Основная точка входа в приложение для управления складом.

Инициализирует базу данных и устанавливает инъекцию зависимостей для сервисного слоя.
"""

from dependency_injector.wiring import inject

from warehouse_management.container import AppContainer
from warehouse_management.domain.services import WarehouseService
from warehouse_management.infrastructure.database import init_db


@inject
def main(container: 'AppContainer') -> None:
    """Главный модуль запуска и настройки приложения.

    Args:
        container: Контейнер зависимостей приложения.
    """
    product_repo = container.product_repository()
    order_repo = container.order_repository()
    uow = container.unit_of_work()

    warehouse_service = WarehouseService(product_repo, order_repo)

    init_db()

    with uow:
        new_product = warehouse_service.create_product(name='Test Product', quantity=5, price=150.0)
        uow.commit()
        print(f'Created product: {new_product}')


if __name__ == '__main__':
    from warehouse_management.settings import Settings

    settings = Settings()
    container = AppContainer()
    container.config.from_pydantic(settings)
    container.wire(modules=[__name__])

    main(container)
