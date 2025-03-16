"""Сервисный слой для управления товарами и заказами."""

from typing import TYPE_CHECKING

from warehouse_management.domain.models import Order, Product

if TYPE_CHECKING:
    from warehouse_management.domain.repositories import OrderRepository, ProductRepository


# TODO: Почему этот модуль находится на слое domain, а не на слое application?
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
            name (str): Название товара.
            quantity (int): Количество товара.
            price (float): Цена товара.

        Returns:
            Product: Созданный товар.
        """
        # TODO: id не может быть None (нужно создать логику генерации ID)
        product = Product(id=None, name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, products: list['Product']) -> 'Order':
        """Создает новый заказ и добавляет его в репозиторий.

        Args:
            products (List[Product]): Список товаров в заказе.

        Returns:
            Order: Созданный заказ.
        """
        # TODO: id не может быть None (нужно создать логику генерации ID)
        order = Order(id=None, products=products)
        self.order_repo.add(order)
        return order
