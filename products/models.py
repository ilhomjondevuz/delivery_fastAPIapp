import datetime

from database import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    Text,
    DateTime,
)

from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False, default=0)

    order_products = relationship(
        "OrderProduct",
        back_populates="product"
    )

    def __repr__(self):
        return f"{self.name} - {self.price}"


class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    order = relationship(
        "Order",
        back_populates="order_products"
    )

    product = relationship(
        "Product",
        back_populates="order_products"
    )

    def __repr__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(Base):
    __tablename__ = "orders"

    ORDER_STATUSES = (
        ("PENDING", "Pending"),
        ("IN_TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    status = Column(
        ChoiceType(choices=ORDER_STATUSES),
        default="PENDING",
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    order_products = relationship(
        "OrderProduct",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    def __repr__(self):
        return f"Order #{self.id} - {self.status}"