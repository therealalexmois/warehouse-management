"""Модели доменного слоя для управления товарами, заказами и клиентами."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Product:
    """Модель товара в системе управления складом.

    Attributes:
        id: Уникальный идентификатор товара (может быть None перед сохранением в БД).
        name: Название товара.
        quantity: Количество товара на складе.
        price: Цена товара.
    """

    id: int | None
    name: str
    quantity: int
    price: float


@dataclass
class Order:
    """Модель заказа, содержащая список товаров или единичный товар.

    Attributes:
        id: Уникальный идентификатор заказа (может быть None перед сохранением в БД).
        customer_id: ID клиента, оформившего заказ (может быть None).
        product: Название товара (если заказ содержит один товар).
        quantity: Количество единиц товара в заказе.
        price: Цена товара.
        products: Список товаров (если заказ содержит несколько товаров).
    """

    id: int | None
    customer_id: int | None
    product: str | None = None
    quantity: int | None = None
    price: float | None = None
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в заказ.

        Args:
            product: Товар, который необходимо добавить в заказ.
        """
        self.products.append(product)

    def get_total_price(self) -> float:
        """Возвращает общую стоимость заказа.

        Returns:
            Общая стоимость заказа.
        """
        if self.products:
            return sum(product.price * product.quantity for product in self.products)

        if self.product and self.quantity and self.price:
            return self.quantity * self.price

        return 0.0


@dataclass
class Customer:
    """Модель клиента в системе управления заказами.

    Attributes:
        id: Уникальный идентификатор клиента (может быть None перед сохранением в БД).
        name: Имя клиента.
        birth_date: Дата рождения клиента.
        orders: Список заказов клиента.
    """

    id: int | None
    name: str
    birth_date: date
    orders: list[Order] = field(default_factory=list)

    def place_order(self, order: Order) -> None:
        """Добавляет заказ к списку заказов клиента.

        Args:
            order: Заказ, который оформляет клиент.
        """
        self.orders.append(order)

    def get_age(self) -> int:
        """Вычисляет возраст клиента на текущий день.

        Returns:
            Возраст клиента в годах.
        """
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
