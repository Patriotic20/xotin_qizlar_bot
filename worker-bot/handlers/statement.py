from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.statement_service import update_statement_status
from utils.keyboards import StatementAction

router = Router()


@router.callback_query(StatementAction.filter())
async def handle_action(
    callback: CallbackQuery,
    callback_data: StatementAction,
    session: AsyncSession,
) -> None:
    stmt = await update_statement_status(
        session=session,
        statement_id=callback_data.statement_id,
        status=callback_data.action,
        operator_id=callback.from_user.id,
    )

    if stmt is None:
        await callback.answer("Ariza topilmadi!", show_alert=True)
        return

    status_label = "✅ Qabul qilindi" if callback_data.action == "accept" else "❌ Rad etildi"
    operator_name = callback.from_user.full_name

    await callback.message.edit_text(
        callback.message.text
        + f"\n\n{status_label}\n👷 Operator: {operator_name}"
    )
    await callback.answer(status_label)
