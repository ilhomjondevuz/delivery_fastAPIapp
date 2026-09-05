from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select

from core.security import get_current_user
from database import Session, engine
from products.models import Product

from products.schemas import OrderProduct, ProductResponse

products_routes = APIRouter(
    prefix="/products",
    tags=["products"],
)

session = Session(bind=engine)

@products_routes.get("/")
async def products_base_api(current_user: str = Depends(get_current_user)) -> dict[str, str]:
    return {
        'message': 'Welcome to products API',
    }

@products_routes.get("/list")
async def products_list_api(
    current_user: str = Depends(get_current_user)
) -> List[ProductResponse]:

    print(current_user)

    result = await session.execute(
        select(Product)
    )

    products = result.scalars().all()
    return products

@products_routes.post("/order/product")
async def order_product(order: OrderProduct, current_user: str = Depends(get_current_user)):
    print(order.product_id)