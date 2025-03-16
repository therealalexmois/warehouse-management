from warehouse_management.container import AppContainer
from warehouse_management.domain.services import WarehouseService
from warehouse_management.infrastructure.database import init_db


def main() -> None:
    """Главный модуль запуска и настройки приложения"""
    init_db()

    product_repo = container.product_repository()
    order_repo = container.order_repository()
    uow = container.unit_of_work()

    warehouse_service = WarehouseService(product_repo, order_repo)

    with uow:
        new_product = warehouse_service.create_product(name='Test Product', quantity=5, price=150.0)
        uow.commit()
        print(f'Created product: {new_product}')


if __name__ == '__main__':
    # TODO: Передать конфиг в container
    # settings = container.settings()
    container = AppContainer()
    main()
