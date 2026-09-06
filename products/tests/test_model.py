import pytest

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from products.models import Product, OrderProduct, Order


@pytest.mark.anyio
async def test_product_order_product_order_models(db, user):
    # Products created
    product_1 = Product(
        name="HP pavilion",
        price=630.00,
    )

    product_2 = Product(
        name="Huawei FOA-LX-9",
        price=320,
    )

    db.add_all([product_1, product_2])

    await db.flush()

    # Order created
    order = Order(
        user=user
    )

    # OrderProducts created
    order_product1 = OrderProduct(
        product=product_1,
        quantity=2,
    )

    order_product2 = OrderProduct(
        product=product_2,
        quantity=3,
    )

    # OrderProducts added to Order
    order.order_products.append(order_product1)
    order.order_products.append(order_product2)

    # Database saved
    db.add(order)

    await db.commit()
    await db.refresh(order)

    # Orderni relationship bilan qayta yuklash
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.order_products)
            .selectinload(OrderProduct.product)
        )
        .where(Order.id == order.id)
    )

    order = result.scalar_one()

    # Checking
    assert user.id is not None

    assert len(order.order_products) == 2

    assert order.order_products[0].product.name == "HP pavilion"
    assert order.order_products[0].quantity == 2

    assert order.order_products[1].product.name == "Huawei FOA-LX-9"
    assert order.order_products[1].quantity == 3