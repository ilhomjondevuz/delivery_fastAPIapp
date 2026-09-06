from products.models import Product, OrderProduct, Order


def test_order_with_order_products(db, user):
    product1 = Product(
        name="iPhone 15",
        price=999.99
    )

    product2 = Product(
        name="AirPods Pro",
        price=249.99
    )

    order = Order(
        user=user,
        order_products=[
            OrderProduct(
                product=product1,
                quantity=2
            ),
            OrderProduct(
                product=product2,
                quantity=1
            )
        ]
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    assert len(order.order_products) == 2

    assert order.order_products[0].product.name == "iPhone 15"
    assert order.order_products[0].quantity == 2

    assert order.order_products[1].product.name == "AirPods Pro"
    assert order.order_products[1].quantity == 1