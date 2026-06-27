import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from models import Base


async def init() -> None:
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("DB tables created successfully")


asyncio.run(init())
