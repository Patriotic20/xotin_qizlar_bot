from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StatementAction(CallbackData, prefix="action"):
    action: str
    statement_id: int


def action_keyboard(statement_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Qabul qilish",
        callback_data=StatementAction(action="accept", statement_id=statement_id),
    )
    builder.button(
        text="❌ Rad etish",
        callback_data=StatementAction(action="reject", statement_id=statement_id),
    )
    builder.adjust(2)
    return builder.as_markup()
