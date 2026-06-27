import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from models.statement import Statement


async def create_statement(
    session: AsyncSession,
    data: dict,
    redis_url: str,
    channel: str,
    file_id: str | None = None,
    file_type: str | None = None,
) -> Statement:
    stmt = Statement(
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
