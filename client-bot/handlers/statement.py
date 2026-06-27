from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from services.statement_service import create_statement
from utils.keyboards import skip_keyboard

router = Router()


class StatementForm(StatesGroup):
    first_name = State()
    last_name = State()
    description = State()


@router.message(F.text == "Murojaat yuborish")
async def start_statement(message: Message, state: FSMContext) -> None:
    await state.set_state(StatementForm.first_name)
    await message.answer(
        "Ismingizni kiriting (ixtiyoriy):",
        reply_markup=skip_keyboard("skip_first_name"),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Murojaat bekor qilindi.")


# --- first_name ---

@router.message(StatementForm.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(StatementForm.last_name)
    await message.answer(
        "Familiyangizni kiriting (ixtiyoriy):",
        reply_markup=skip_keyboard("skip_last_name"),
    )


@router.callback_query(StatementForm.first_name, F.data == "skip_first_name")
async def skip_first_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(first_name=None)
    await state.set_state(StatementForm.last_name)
    await callback.message.edit_text(
        "Familiyangizni kiriting (ixtiyoriy):",
        reply_markup=skip_keyboard("skip_last_name"),
    )
    await callback.answer()


# --- last_name ---

@router.message(StatementForm.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(StatementForm.description)
    await message.answer("✍️ Nima bo'lganini batafsil yozing:")


@router.callback_query(StatementForm.last_name, F.data == "skip_last_name")
async def skip_last_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(last_name=None)
    await state.set_state(StatementForm.description)
    await callback.message.edit_text("✍️ Nima bo'lganini batafsil yozing:")
    await callback.answer()


# --- description → submit ---

@router.message(StatementForm.description)
async def process_description(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    await state.clear()
    stmt = await create_statement(
        session=session,
        data={**data, "description": message.text},
        redis_url=settings.redis_url,
        channel=settings.redis_channel,
        client_tg_id=message.from_user.id,
    )
    await message.answer(
        f"✅ #{stmt.id} Murojaat qabul qilindi.\n\n"
        "Rahmat. Administratorlar uni tez orada ko'rib chiqishadi."
    )
