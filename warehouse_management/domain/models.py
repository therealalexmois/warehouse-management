"""Модели доменного слоя для управления товарами и заказами."""

from dataclasses import dataclass, field


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
    """Модель заказа, содержащая список товаров.

    Attributes:
        id: Уникальный идентификатор заказа (может быть None перед сохранением в БД).
        products: Список товаров в заказе.
    """

    id: int | None
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в заказ.

        Args:
            product: Товар, который необходимо добавить в заказ.
        """
        self.products.append(product)
