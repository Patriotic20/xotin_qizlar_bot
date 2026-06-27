from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message  # CallbackQuery used for file skip
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from services.statement_service import create_statement
from utils.keyboards import skip_keyboard

router = Router()


class StatementForm(StatesGroup):
    description = State()
    file = State()


@router.message(F.text == "Murojaat yuborish")
async def start_statement(message: Message, state: FSMContext) -> None:
    await state.set_state(StatementForm.description)
    await message.answer(
        "✍️ Nima bo'lganini batafsil yozing.\n\n"
        "Bekor qilish uchun /cancel yozing."
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Murojaat bekor qilindi.")


@router.message(StatementForm.description)
async def process_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(StatementForm.file)
    await message.answer(
        "📎 Dalil sifatida foto, video yoki hujjat biriktiring (ixtiyoriy).\n\n"
        "Bekor qilish uchun /cancel yozing.",
        reply_markup=skip_keyboard(),
    )


async def _submit(
    session: AsyncSession,
    state: FSMContext,
    file_id: str | None,
    file_type: str | None,
) -> int:
    data = await state.get_data()
    await state.clear()
    stmt = await create_statement(
        session=session,
        data=data,
        file_id=file_id,
        file_type=file_type,
        redis_url=settings.redis_url,
        channel=settings.redis_channel,
    )
    return stmt.id


@router.message(StatementForm.file, F.photo)
async def process_photo(message: Message, state: FSMContext, session: AsyncSession) -> None:
    stmt_id = await _submit(session, state, message.photo[-1].file_id, "photo")
    await message.answer(
        f"✅ #{stmt_id} Murojaat qabul qilindi.\n\n"
        "Rahmat. Administratorlar uni tez orada ko'rib chiqishadi."
    )


@router.message(StatementForm.file, F.video)
async def process_video(message: Message, state: FSMContext, session: AsyncSession) -> None:
    stmt_id = await _submit(session, state, message.video.file_id, "video")
    await message.answer(
        f"✅ #{stmt_id} Murojaat qabul qilindi.\n\n"
        "Rahmat. Administratorlar uni tez orada ko'rib chiqishadi."
    )


@router.message(StatementForm.file, F.document)
async def process_document(message: Message, state: FSMContext, session: AsyncSession) -> None:
    stmt_id = await _submit(session, state, message.document.file_id, "document")
    await message.answer(
        f"✅ #{stmt_id} Murojaat qabul qilindi.\n\n"
        "Rahmat. Administratorlar uni tez orada ko'rib chiqishadi."
    )


@router.callback_query(StatementForm.file, F.data == "skip_file")
async def process_skip_file(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    stmt_id = await _submit(session, state, None, None)
    await callback.message.edit_text(
        f"✅ #{stmt_id} Murojaat qabul qilindi.\n\n"
        "Rahmat. Administratorlar uni tez orada ko'rib chiqishadi."
    )
    await callback.answer()
