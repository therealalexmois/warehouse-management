"""Абстрактные интерфейсы репозиториев для работы с товарами и заказами."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from warehouse_management.domain.models import Order, Product


# TODO: Почему тут используется абстрактный класс, а не Protocol?
class ProductRepository(ABC):
    """Абстрактный репозиторий для управления товарами."""

    @abstractmethod
    def add(self, product: 'Product') -> None:
        """Добавляет товар в репозиторий.

        Args:
            product (Product): Товар для добавления.
        """
        pass

    @abstractmethod
    def get(self, product_id: int) -> 'Product':
        """Получает товар по его ID.

        Args:
            product_id (int): Идентификатор товара.

        Returns:
            Product: Найденный товар.
        """
        pass

    @abstractmethod
    def list(self) -> list['Product']:
        """Возвращает список всех товаров.

        Returns:
            List[Product]: Список товаров.
        """
        pass


class OrderRepository(ABC):
    """Абстрактный репозиторий для управления заказами."""

    @abstractmethod
    def add(self, order: 'Order') -> None:
        """Добавляет заказ в репозиторий.

        Args:
            order (Order): Заказ для добавления.
        """
        pass

    @abstractmethod
    def get(self, order_id: int) -> 'Order':
        """Получает заказ по его ID.

        Args:
            order_id (int): Идентификатор заказа.

        Returns:
            Order: Найденный заказ.
        """
        pass

    @abstractmethod
    def list(self) -> list['Order']:
        """Возвращает список всех заказов.

        Returns:
            List[Order]: Список заказов.
        """
        pass
