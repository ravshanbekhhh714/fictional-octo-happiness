from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from db.database import async_session
from db.crud import get_candidate_by_telegram_id

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with async_session() as db:
        candidate = await get_candidate_by_telegram_id(db, message.from_user.id)
        if candidate:
            await message.answer(f"Siz allaqachon ro'yxatdan o'tgansiz. Holatingiz: {candidate.status}")
            return

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ha ✅"), KeyboardButton(text="Yo'q ❌")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}! ITLIVE Academy HR botiga xush kelibsiz.\n"
        "Nomzod sifatida ro'yxatdan o'tmoqchimisiz?",
        reply_markup=kb
    )

@router.message(Command("test_ai"))
async def cmd_test_ai(message: Message):
    from core.ai_evaluator import call_ai
    await message.answer("AI ulanishi tekshirilmoqda... ⏳")
    try:
        resp = await call_ai("Salom, kimsan?", system="Qisqa javob ber.")
        if resp:
            await message.answer(f"✅ AI ishlamoqda!\nJavob: {resp}")
        else:
            await message.answer("❌ AI javob bermadi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik: `{str(e)}`")
