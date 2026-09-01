import asyncio
from database import engine, Base

async def init_db():
    import accounts.models
    import products.models
    async with engine.begin() as conn:
        # run_sync orqali jadvallarni yaratish
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())