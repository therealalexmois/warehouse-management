"""End-to-End тесты для всего приложения."""

from typing import TYPE_CHECKING

import pytest

from warehouse_management.domain.services import WarehouseService

if TYPE_CHECKING:
    from warehouse_management.infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository


@pytest.fixture
def warehouse_service(
    product_repo: 'SqlAlchemyProductRepository', order_repo: 'SqlAlchemyOrderRepository'
) -> 'WarehouseService':
    """Создает сервис управления складом, используя реальные зависимости."""
    return WarehouseService(product_repo, order_repo)


@pytest.mark.e2e
@pytest.mark.parametrize(
    'name, quantity, price',
    [
        ('E2E Laptop', 20, 1599.99),
        ('E2E Phone', 15, 899.50),
        ('E2E Tablet', 10, 499.99),
    ],
)
def test_create_product__e2e(
    warehouse_service: 'WarehouseService',
    product_repo: 'SqlAlchemyProductRepository',
    name: str,
    quantity: int,
    price: float,
) -> None:
    """Тест полного создания продукта.

    Ожидаемый результат:
    - Продукт успешно создается и сохраняется в базе.
    """
    product = warehouse_service.create_product(name=name, quantity=quantity, price=price)

    assert product.name == name
    assert product.quantity == quantity
    assert product.price == price

    assert product.id is not None, 'Product ID must not be None after saving'
    stored_product = product_repo.get(int(product.id))
    assert stored_product is not None
    assert stored_product.name == name
    assert stored_product.quantity == quantity
    assert stored_product.price == price


@pytest.mark.e2e
def test_create_order__e2e(warehouse_service: 'WarehouseService') -> None:
    """Тест создания заказа с несколькими продуктами.

    Ожидаемый результат:
    - Заказ успешно создается и связывается с продуктами.
    """
    product1 = warehouse_service.create_product(name='E2E Product 1', quantity=5, price=99.99)
    product2 = warehouse_service.create_product(name='E2E Product 2', quantity=3, price=49.99)

    expected_product_count = 2

    order = warehouse_service.create_order([product1, product2])

    assert len(order.products) == expected_product_count, f'Order должен содержать {expected_product_count} продукта'
    assert order.products[0].name == 'E2E Product 1'
    assert order.products[1].name == 'E2E Product 2'
