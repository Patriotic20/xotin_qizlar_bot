import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from models.statement import Statement


async def create_statement(
    session: AsyncSession,
    data: dict,
    redis_url: str,
    channel: str,
    client_tg_id: int | None = None,
    file_id: str | None = None,
    file_type: str | None = None,
) -> Statement:
    stmt = Statement(
        client_tg_id=client_tg_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        description=data["description"],
        file_id=file_id,
        file_type=file_type,
        status="pending",
    )
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)

    redis = aioredis.from_url(redis_url)
    await redis.publish(channel, str(stmt.id))
    await redis.aclose()

    return stmt
