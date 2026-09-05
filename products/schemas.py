from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    photo_url: str
    price: float

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {
            "id": 1,
            "name": "Notebook",
            "description": "Beautiful notebook",
            "photo_url": "https://delivery.ilhomjon.uz/media/product/notebook.jpg",
            "price": 0.0,
        }},
    )

class OrderProduct(BaseModel):
    product_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"product_id": 1}},
    )