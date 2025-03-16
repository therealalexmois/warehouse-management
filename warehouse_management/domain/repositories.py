"""Абстрактные интерфейсы репозиториев для работы с товарами и заказами."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from warehouse_management.domain.models import Order, Product


class ProductRepository(ABC):
    """Абстрактный репозиторий для управления товарами."""

    @abstractmethod
    def add(self, product: 'Product') -> None:
        """Добавляет товар в репозиторий.

        Args:
            product: Товар для добавления.
        """
        pass

    @abstractmethod
    def get(self, product_id: int) -> 'Product':
        """Получает товар по его ID.

        Args:
            product_id: Идентификатор товара.

        Returns:
            Найденный товар.
        """
        pass

    @abstractmethod
    def list(self) -> list['Product']:
        """Возвращает список всех товаров.

        Returns:
            Список товаров.
        """
        pass


class OrderRepository(ABC):
    """Абстрактный репозиторий для управления заказами."""

    @abstractmethod
    def add(self, order: 'Order') -> None:
        """Добавляет заказ в репозиторий.

        Args:
            order: Заказ для добавления.
        """
        pass

    @abstractmethod
    def get(self, order_id: int) -> 'Order':
        """Получает заказ по его ID.

        Args:
            order_id: Идентификатор заказа.

        Returns:
            Найденный заказ.
        """
        pass

    @abstractmethod
    def list(self) -> list['Order']:
        """Возвращает список всех заказов.

        Returns:
            Список заказов.
        """
        pass
