from dataclasses import dataclass, field


@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float


@dataclass
class Order:
    id: int
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)
