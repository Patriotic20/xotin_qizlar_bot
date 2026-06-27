import asyncio
import json

import redis.asyncio as aioredis
from aiogram import Bot
from loguru import logger


async def reply_listener(bot: Bot, redis_url: str, channel: str) -> None:
    while True:
        try:
            redis = aioredis.from_url(redis_url)
            pubsub = redis.pubsub()
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to Redis reply channel: {channel}")

            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                data = json.loads(message["data"])
                client_tg_id = data["client_tg_id"]
                statement_id = data["statement_id"]
                reply_text = data["reply"]

                try:
                    await bot.send_message(
                        client_tg_id,
                        f"📩 #{statement_id} murojaatingizga javob:\n\n{reply_text}",
                    )
                except Exception as e:
                    logger.error(f"Failed to deliver reply to {client_tg_id}: {e}")

        except asyncio.CancelledError:
            logger.info("Reply listener cancelled")
            return
        except Exception as e:
            logger.error(f"Reply listener error: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)
