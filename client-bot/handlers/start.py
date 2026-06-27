from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

router = Router()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Murojaat yuborish")]],
    resize_keyboard=True,
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "🤝 Assalomu alaykum!\n\n"
        "Bu bot NDKTU ayol xodimlari va talabalari uchun mo'ljallangan.\n\n"
        "Талаба қизларга нисбатан шилқимлик, тазйиқ ва зўравонлик ҳолатларини олдини олиш учун ташкил этилди (https://www.lex.uz/docs/8070193).\n\n"
        "Agar siz:\n"
        "• Jinsiy ta'qib yoki zo'ravonlikka duch kelgan bo'lsangiz\n"
        "• Psixologik bosim yoki kamsitishga uchragan bo'lsangiz\n"
        "• Yordamga muhtoj bo'lsangiz\n\n"
        "— bu yerda xavfsiz va anonim ravishda murojaat qilishingiz mumkin.\n\n"
        "🔒 Siz mutlaqo anonimsiiz. Hech qanday shaxsiy ma'lumot so'ralmaydi.",
        reply_markup=main_keyboard,
    )
