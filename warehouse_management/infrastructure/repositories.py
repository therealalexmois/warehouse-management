"""Репозитории для взаимодействия с базой данных через SQLAlchemy."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from warehouse_management.domain.exceptions import NotFoundError
from warehouse_management.domain.models import Order, Product
from warehouse_management.domain.repositories import OrderRepository, ProductRepository
from warehouse_management.infrastructure.orm import OrderORM, ProductORM


class SqlAlchemyProductRepository(ProductRepository):
    """Репозиторий для управления товарами."""

    def __init__(self, session: 'Session') -> None:
        """Инициализирует репозиторий товаров.

        Args:
            session: Экземпляр SQLAlchemy-сессии.
        """
        self.session = session

    def add(self, product: 'Product') -> None:
        """Добавляет товар в базу данных.

        Args:
            product: Экземпляр товара.
        """
        product_orm = ProductORM(name=product.name, quantity=product.quantity, price=product.price)
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id

    def get(self, product_id: int) -> 'Product | None':
        """Получает товар по ID.

        Args:
            product_id: Идентификатор товара.

        Returns:
            Найденный товар или None, если товар отсутствует.
        """
        if product_id < 0:
            raise ValueError('Product ID must be a positive integer')

        product_orm = self.session.query(ProductORM).filter_by(id=product_id).first()
        if product_orm is None:
            raise NotFoundError(f'Product with ID {product_id} not found')

        return Product(id=product_orm.id, name=product_orm.name, quantity=product_orm.quantity, price=product_orm.price)

    def list(self) -> list['Product']:
        """Возвращает список всех товаров.

        Returns:
            Список товаров.
        """
        products_orm = self.session.query(ProductORM).all()
        return [Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in products_orm]


class SqlAlchemyOrderRepository(OrderRepository):
    """Репозиторий для управления заказами через SQLAlchemy."""

    def __init__(self, session: 'Session') -> None:
        """Инициализирует репозиторий заказов.

        Args:
            session: Экземпляр SQLAlchemy-сессии.
        """
        self.session = session

    def add(self, order: Order) -> None:
        """Добавляет заказ в базу данных.

        Args:
            order: Экземпляр заказа.
        """
        order_orm = OrderORM()
        order_orm.products = [self.session.query(ProductORM).filter_by(id=p.id).one() for p in order.products]
        self.session.add(order_orm)

    def get(self, order_id: int) -> Order | None:
        """Получает заказ по ID.

        Args:
            order_id: Идентификатор заказа.

        Returns:
            Найденный заказ или None, если заказ отсутствует.
        """
        order_orm = self.session.query(OrderORM).filter_by(id=order_id).one_or_none()
        if not order_orm:
            return None
        products = [Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in order_orm.products]
        return Order(id=order_orm.id, products=products)

    def list(self) -> list[Order]:
        """Возвращает список всех заказов.

        Returns:
            Список заказов.
        """
        orders_orm = self.session.query(OrderORM).all()
        return [
            Order(
                id=order_orm.id,
                products=[
                    Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in order_orm.products
                ],
            )
            for order_orm in orders_orm
        ]
