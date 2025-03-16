"""Интеграционные тесты для ORM-моделей."""

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.exc import IntegrityError

from warehouse_management.infrastructure.orm import OrderORM, ProductORM

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@pytest.mark.integration
@pytest.mark.parametrize(
    'name, quantity, price',
    [
        ('ORM Laptop', 10, 1299.99),
        ('ORM Smartphone', 5, 799.99),
        ('ORM Tablet', 7, 499.99),
    ],
)
def test_product_orm__insert(db_session: 'Session', name: str, quantity: int, price: float) -> None:
    """Тест успешного добавления продукта через ORM.

    Ожидаемый результат:
    - Продукт успешно сохраняется в базе.
    """
    product = ProductORM(name=name, quantity=quantity, price=price)
    db_session.add(product)
    db_session.commit()

    result = db_session.query(ProductORM).filter_by(name=name).one()

    assert result is not None
    assert result.name == name
    assert result.quantity == quantity
    assert result.price == price


@pytest.mark.integration
@pytest.mark.parametrize(
    'name, quantity, price',
    [
        (None, 5, 1299.99),
        ('Laptop', None, 1299.99),
        ('Laptop', 5, None),
        (None, None, None),
    ],
)
def test_product_orm__constraint_violation(
    db_session: 'Session', name: str | None, quantity: int | None, price: float | None
) -> None:
    """Тест ошибки нарушения ограничения NOT NULL.

    Ожидаемый результат:
    - SQLAlchemy выбрасывает `IntegrityError` при добавлении `None` в NOT NULL колонку.
    """
    product = ProductORM(name=name, quantity=quantity, price=price)
    db_session.add(product)

    with pytest.raises(IntegrityError):
        db_session.commit()


@pytest.mark.integration
@pytest.mark.parametrize(
    'products',
    [
        [
            {'name': 'Product 1', 'quantity': 5, 'price': 100.0},
            {'name': 'Product 2', 'quantity': 2, 'price': 50.0},
        ],
        [
            {'name': 'Product A', 'quantity': 3, 'price': 150.0},
            {'name': 'Product B', 'quantity': 1, 'price': 75.0},
            {'name': 'Product C', 'quantity': 10, 'price': 20.0},
        ],
        [
            {'name': 'Single Item', 'quantity': 1, 'price': 999.99},
        ],
    ],
)
def test_order_orm__create_with_products(db_session: 'Session', products: list[dict[str, float]]) -> None:
    """Тест успешного создания заказа с продуктами.

    Ожидаемый результат:
    - Заказ сохраняется в базе.
    - Продукты связываются с заказом.
    """
    product_orms = [ProductORM(**product) for product in products]

    order = OrderORM()
    order.products = product_orms

    db_session.add_all(product_orms + [order])
    db_session.commit()

    result = db_session.query(OrderORM).filter_by(id=order.id).one()
    assert result is not None
    assert len(result.products) == len(products)

    for product, expected in zip(result.products, products, strict=True):
        assert product.name == expected['name']
        assert product.quantity == expected['quantity']
        assert product.price == expected['price']
