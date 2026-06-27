from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.operator import Operator
from models.statement import Statement


async def get_statement(session: AsyncSession, statement_id: int) -> Statement | None:
    result = await session.execute(
        select(Statement).where(Statement.id == statement_id)
    )
    return result.scalar_one_or_none()


async def get_active_operators(session: AsyncSession) -> list[Operator]:
    result = await session.execute(
        select(Operator).where(Operator.is_active == True)  # noqa: E712
    )
    return list(result.scalars().all())


async def update_statement_status(
    session: AsyncSession,
    statement_id: int,
    status: str,
    operator_id: int,
) -> Statement | None:
    stmt = await get_statement(session, statement_id)
    if stmt is None:
        return None
    stmt.status = status
    stmt.operator_id = operator_id
    await session.commit()
    await session.refresh(stmt)
    return stmt
