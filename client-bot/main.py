import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from handlers.start import router as start_router
from handlers.statement import router as statement_router
from middlewares.db import DbSessionMiddleware
from services.reply_listener import reply_listener
from utils.logger import setup_logger


async def main() -> None:
    setup_logger()

    engine = create_async_engine(settings.database_url, echo=False)
    session_pool = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=settings.bot_token)
    storage = RedisStorage.from_url(settings.redis_url)
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware(session_pool))
    dp.include_router(start_router)
    dp.include_router(statement_router)

    reply_task = asyncio.create_task(
        reply_listener(bot, settings.redis_url, settings.redis_reply_channel)
    )

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        reply_task.cancel()
        await asyncio.gather(reply_task, return_exceptions=True)
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
