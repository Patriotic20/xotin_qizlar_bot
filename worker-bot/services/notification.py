import asyncio
from datetime import timedelta

import redis.asyncio as aioredis
from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker

from models.statement import Statement
from services.statement_service import get_active_operators, get_statement
from utils.keyboards import reply_keyboard


def format_statement(stmt: Statement) -> str:
    name_parts = [stmt.first_name, stmt.last_name]
    name = " ".join(p for p in name_parts if p)
    name_line = f"👤 {name}\n" if name else ""
    display_time = stmt.created_at + timedelta(hours=5)
    return (
        f"🆘 Yangi murojaat #{stmt.id}\n\n"
        f"{name_line}"
        f"📝 {stmt.description}\n\n"
        f"🕐 {display_time.strftime('%d.%m.%Y %H:%M')} (Toshkent)"
    )


async def _notify_operators(bot: Bot, stmt: Statement, operators: list) -> None:
    text = format_statement(stmt)
    kb = reply_keyboard(stmt.id)

    for op in operators:
        try:
            if stmt.file_id and stmt.file_type == "photo":
                await bot.send_photo(op.telegram_id, stmt.file_id, caption=text, reply_markup=kb)
            elif stmt.file_id and stmt.file_type == "video":
                await bot.send_video(op.telegram_id, stmt.file_id, caption=text, reply_markup=kb)
            elif stmt.file_id and stmt.file_type == "document":
                await bot.send_document(op.telegram_id, stmt.file_id, caption=text, reply_markup=kb)
            else:
                await bot.send_message(op.telegram_id, text, reply_markup=kb)
        except Exception as e:
            logger.error(f"Failed to notify operator {op.telegram_id}: {e}")


async def statement_listener(
    bot: Bot,
    redis_url: str,
    channel: str,
    session_pool: async_sessionmaker,
) -> None:
    while True:
        try:
            redis = aioredis.from_url(redis_url)
            pubsub = redis.pubsub()
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to Redis channel: {channel}")

            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                statement_id = int(message["data"])
                logger.info(f"Received new statement ID: {statement_id}")

                async with session_pool() as session:
                    stmt = await get_statement(session, statement_id)
                    if stmt is None:
                        logger.warning(f"Statement {statement_id} not found in DB")
                        continue
                    operators = await get_active_operators(session)

                if not operators:
                    logger.warning("No active operators to notify")
                    continue

                await _notify_operators(bot, stmt, operators)

        except asyncio.CancelledError:
            logger.info("Statement listener cancelled")
            return
        except Exception as e:
            logger.error(f"Redis listener error: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)
