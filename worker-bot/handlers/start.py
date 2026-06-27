from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.operator import Operator

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession) -> None:
    result = await session.execute(
        select(Operator).where(Operator.telegram_id == message.from_user.id)
    )
    operator = result.scalar_one_or_none()

    if operator is None:
        operator = Operator(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            is_active=True,
        )
        session.add(operator)
        await session.commit()
        await message.answer(
            f"Salom, {message.from_user.full_name}! 👋\n\n"
            "Siz operator sifatida ro'yxatdan o'tdingiz.\n"
            "Endi sizga yangi arizalar keladi."
        )
    else:
        await message.answer(
            f"Salom, {message.from_user.full_name}! 👋\n\n"
            f"Siz allaqachon operator sifatida ro'yxatdan o'tgansiz.\n"
            f"Holat: {'✅ Faol' if operator.is_active else '❌ Nofaol'}"
        )
