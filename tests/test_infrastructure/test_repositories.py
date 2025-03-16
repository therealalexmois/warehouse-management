"""Интеграционные тесты для SQLAlchemy репозиториев."""

from typing import TYPE_CHECKING

import pytest

from warehouse_management.domain.exceptions import NotFoundError
from warehouse_management.infrastructure.orm import ProductORM

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from warehouse_management.infrastructure.repositories import SqlAlchemyProductRepository


@pytest.mark.integration
@pytest.mark.parametrize(
    'name, quantity, price',
    [
        ('Laptop', 5, 1500.0),
        ('Phone', 10, 700.5),
    ],
)
def test_product_repository__add_and_get(
    product_repo: 'SqlAlchemyProductRepository',
    db_session: 'Session',
    name: str,
    quantity: int,
    price: float,
) -> None:
    """Тест добавления и получения продукта в репозитории.

    Ожидаемый результат:
    - Продукт успешно сохраняется и извлекается.
    """
    product_orm = ProductORM(name=name, quantity=quantity, price=price)

    db_session.add(product_orm)
    db_session.commit()
    db_session.refresh(product_orm)

    assert product_orm.id is not None, 'ID должен быть присвоен после коммита'

    fetched_product = product_repo.get(product_orm.id)
    assert fetched_product is not None
    assert fetched_product.name == name
    assert fetched_product.quantity == quantity
    assert fetched_product.price == price


@pytest.mark.integration
@pytest.mark.parametrize(
    'invalid_id, expected_exception',
    [
        (-1, ValueError),
        (1000, NotFoundError),
    ],
)
def test_product_repository__get_invalid_id(
    product_repo: 'SqlAlchemyProductRepository',
    invalid_id: int,
    expected_exception: type[Exception],
) -> None:
    """Тест обработки несуществующего ID продукта.

    Ожидаемый результат:
    - Выбрасывается ожидаемое исключение при запросе несуществующего ID.
    """
    with pytest.raises(expected_exception):
        product_repo.get(invalid_id)
