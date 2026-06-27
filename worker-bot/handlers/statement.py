import json

import redis.asyncio as aioredis
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from services.statement_service import get_statement
from utils.keyboards import ReplyAction

router = Router()


class ReplyForm(StatesGroup):
    reply_text = State()


@router.callback_query(ReplyAction.filter())
async def ask_reply(
    callback: CallbackQuery,
    callback_data: ReplyAction,
    state: FSMContext,
) -> None:
    await state.update_data(statement_id=callback_data.statement_id)
    await state.set_state(ReplyForm.reply_text)
    await callback.message.answer("✍️ Javobingizni yozing:")
    await callback.answer()


@router.message(ReplyForm.reply_text)
async def send_reply(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    data = await state.get_data()
    statement_id = data["statement_id"]
    await state.clear()

    stmt = await get_statement(session, statement_id)
    if stmt is None or stmt.client_tg_id is None:
        await message.answer("Murojaat topilmadi yoki mijoz anonim.")
        return

    redis = aioredis.from_url(settings.redis_url)
    payload = json.dumps({
        "client_tg_id": stmt.client_tg_id,
        "statement_id": statement_id,
        "reply": message.text,
    })
    await redis.publish(settings.redis_reply_channel, payload)
    await redis.aclose()

    await message.answer(f"✅ #{statement_id} Javob yuborildi.")
