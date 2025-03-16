"""Модуль ORM-моделей для работы с базой данных."""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс ORM для SQLAlchemy."""

    pass


class ProductORM(Base):
    """Модель товара в базе данных."""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)


order_product_associations = Table(
    'order_product_associations',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id')),
    Column('product_id', ForeignKey('products.id')),
)


class OrderORM(Base):
    """Модель заказа в базе данных."""

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    products = relationship('ProductORM', secondary=order_product_associations)
