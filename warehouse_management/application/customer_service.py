"""Сервис для управления клиентами и их заказами."""

from typing import TYPE_CHECKING

from warehouse_management.domain.models import Customer, Order

if TYPE_CHECKING:
    from datetime import date

    from warehouse_management.domain.repositories import CustomerRepository, OrderRepository


class CustomerService:
    """Обрабатывает бизнес-логику управления клиентами."""

    def __init__(self, customer_repo: 'CustomerRepository', order_repo: 'OrderRepository') -> None:
        """Инициализирует сервис клиентов.

        Args:
            customer_repo: Репозиторий для хранения клиентов.
            order_repo: Репозиторий для хранения заказов.
        """
        self.customer_repo = customer_repo
        self.order_repo = order_repo

    def register_customer(self, name: str, birth_date: 'date') -> Customer:
        """Регистрирует нового клиента.

        Args:
            name: Имя клиента.
            birth_date: Дата рождения клиента.

        Returns:
            Зарегистрированный клиент.
        """
        new_customer = Customer(id=None, name=name, birth_date=birth_date)
        self.customer_repo.add(new_customer)
        return new_customer

    def create_order(self, customer_id: int, order_id: int, product: str, quantity: int, price: float) -> Order:
        """Создаёт заказ для существующего клиента.

        Args:
            customer_id: ID клиента, оформляющего заказ.
            order_id: ID заказа.
            product: Название товара.
            quantity: Количество товара.
            price: Цена за единицу.

        Returns:
            Созданный заказ.

        Raises:
            ValueError: Если клиент не найден.
        """
        customer = self.customer_repo.get(customer_id)
        if not customer:
            raise ValueError(f'Клиент с ID {customer_id} не найден')

        new_order = Order(
            id=order_id,
            customer_id=customer_id,  # ✅ Now correctly passing the customer ID
            product=product,
            quantity=quantity,
            price=price,
        )
        customer.place_order(new_order)
        self.order_repo.add(new_order)

        return new_order

    def get_customer_info(self, customer_id: int) -> dict:
        """Возвращает информацию о клиенте.

        Args:
            customer_id: ID клиента.

        Returns:
            Словарь с информацией о клиенте и его заказах.

        Raises:
            ValueError: Если клиент не найден.
        """
        customer = self.customer_repo.get(customer_id)
        if not customer:
            raise ValueError(f'Клиент с ID {customer_id} не найден')

        return {
            'id': customer.id,
            'name': customer.name,
            'age': customer.get_age(),
            'orders': [
                {
                    'id': order.id,
                    'product': order.product,
                    'quantity': order.quantity,
                    'price': order.price,
                    'total_price': order.get_total_price(),
                }
                for order in customer.orders
            ],
        }
