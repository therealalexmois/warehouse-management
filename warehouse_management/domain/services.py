"""Сервисный слой для управления товарами и заказами."""

from typing import TYPE_CHECKING

from warehouse_management.domain.models import Order, Product

if TYPE_CHECKING:
    from warehouse_management.domain.repositories import OrderRepository, ProductRepository


class WarehouseService:
    """Сервис управления складом.

    Этот класс управляет созданием товаров и заказов, взаимодействуя с репозиториями.
    """

    def __init__(self, product_repo: 'ProductRepository', order_repo: 'OrderRepository') -> None:
        """Инициализирует сервис склада.

        Args:
            product_repo: Репозиторий товаров.
            order_repo: Репозиторий заказов.
        """
        self.product_repo = product_repo
        self.order_repo = order_repo

    def create_product(self, name: str, quantity: int, price: float) -> 'Product':
        """Создает новый товар и добавляет его в репозиторий.

        Args:
            name: Название товара.
            quantity: Количество товара.
            price: Цена товара.

        Returns:
            Созданный товар.

        Raises:
            ValueError: Если `name` пустой, `quantity` < 0 или `price` < 0.
        """
        if not name.strip():
            raise ValueError('Название продукта не может быть пустым')
        if quantity < 0:
            raise ValueError('Количество продукта не может быть отрицательным')
        if price < 0:
            raise ValueError('Цена продукта не может быть отрицательной')

        product = Product(id=None, name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, products: list['Product']) -> 'Order':
        """Создает новый заказ и добавляет его в репозиторий.

        Args:
            products: Список товаров в заказе.

        Returns:
            Созданный заказ.
        """
        order = Order(id=None, products=products)
        self.order_repo.add(order)
        return order
