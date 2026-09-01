from fastapi import FastAPI
from accounts.routes import accounts_routes
from products.routes import products_routes

app = FastAPI()
app.include_router(accounts_routes)
app.include_router(products_routes)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}