from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ReplyAction(CallbackData, prefix="reply"):
    statement_id: int


def reply_keyboard(statement_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💬 Javob berish",
        callback_data=ReplyAction(statement_id=statement_id),
    )
    return builder.as_markup()
