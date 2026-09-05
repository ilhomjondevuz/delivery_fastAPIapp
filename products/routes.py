from fastapi import APIRouter

products_routes = APIRouter(
    prefix="/products",
    tags=["products"],
)

@products_routes.get("/")
async def products_base_api() -> dict[str, str]:
    return {
        'message': 'Welcome to products API',
    }