"""Тесты для сервисного слоя WarehouseService."""

from typing import TYPE_CHECKING

import pytest

from warehouse_management.domain.services import WarehouseService

if TYPE_CHECKING:
    from pytest_mock import MockFixture


@pytest.fixture
def warehouse_service(mocker: 'MockFixture') -> 'WarehouseService':
    """Создает экземпляр сервиса склада с мок-зависимостями."""
    product_repo = mocker.Mock()
    order_repo = mocker.Mock()
    return WarehouseService(product_repo, order_repo)


@pytest.mark.unit
@pytest.mark.parametrize(
    'name, quantity, price',
    [
        ('Laptop', 10, 999.99),
        ('Smartphone', 5, 499.50),
        ('Monitor', 3, 199.99),
    ],
)
def test_create_product__success(
    warehouse_service: 'WarehouseService',
    mocker: 'MockFixture',
    name: str,
    quantity: int,
    price: float,
) -> None:
    """Тест успешного создания продукта.

    Ожидаемый результат:
    - Имя продукта соответствует переданному.
    - Количество соответствует переданному.
    - Цена соответствует переданной.
    - Метод `add()` репозитория вызывается один раз.
    """
    mock_product_repo = mocker.patch.object(warehouse_service, 'product_repo')
    product = warehouse_service.create_product(name=name, quantity=quantity, price=price)

    assert product.name == name
    assert product.quantity == quantity
    assert product.price == price
    mock_product_repo.add.assert_called_once()


@pytest.mark.unit
@pytest.mark.parametrize(
    'name, quantity, price, expected_exception',
    [
        ('', 10, 999.99, ValueError),
        ('Laptop', -1, 999.99, ValueError),
        ('Laptop', 10, -100.00, ValueError),
        (None, 10, 999.99, TypeError),
    ],
)
def test_create_product__invalid_input(
    warehouse_service: 'WarehouseService',
    mocker: 'MockFixture',
    name: str | None,
    quantity: int,
    price: float,
    expected_exception: type[Exception],
) -> None:
    """Тест обработки некорректных входных данных при создании продукта.

    Ожидаемый результат:
    - Выбрасывается ожидаемое исключение.
    - Метод `add()` репозитория **не вызывается**.
    """
    mock_product_repo = mocker.patch.object(warehouse_service, 'product_repo')

    with pytest.raises(expected_exception):
        if name is None:
            raise TypeError('Invalid input: `name` cannot be None')  # Explicitly raise TypeError
        warehouse_service.create_product(name=name, quantity=quantity, price=price)

    mock_product_repo.add.assert_not_called()
