import asyncio
import logging
import json
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_TOKEN = "8529363243:AAF6FeK5N8TVvv9YgaK7uM-RQUUgDi0uEHY"
ADMIN_ID = 6482915822

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def get_balance(user_id):
    db = load_db()
    return db.get(str(user_id), {}).get("balance", 0)

def add_balance(user_id, amount):
    db = load_db()
    str_id = str(user_id)
    if str_id not in db:
        db[str_id] = {"balance": 0}
    db[str_id]["balance"] += amount
    save_db(db)
    return db[str_id]["balance"]

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    bal = get_balance(user_id)
    await message.answer(
        f"Xush kelibsiz, {message.from_user.first_name}!\n\n"
        f"💰 **Sizning balansingiz:** {bal:,} so'm\n\n"
        f"**FUNGO SHOP** do'konidan foydalanish uchun pastdagi menyu tugmasini bosing."
    )

@dp.message(Command("addbal"))
async def add_balance_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split()
        target_user_id = int(args[1])
        amount = int(args[2])

        new_bal = add_balance(target_user_id, amount)

        await message.answer(f"✅ ID: `{target_user_id}` balansiga **{amount:,} so'm** qo'shildi!\nYangi balans: **{new_bal:,} so'm**")

        try:
            await bot.send_message(
                chat_id=target_user_id,
                text=f"💳 **Balans to'ldirildi!**\n\nHisobingizga **{amount:,} so'm** qo'shildi.\nJoriy balansingiz: **{new_bal:,} so'm**"
            )
        except Exception:
            await message.answer("⚠️ Mijozga xabar yetib bormadi.")

    except (IndexError, ValueError):
        await message.answer("❌ Xato format!\nTo'g'ri yozish: `/addbal USER_ID SUMMA`\nMasalan: `/addbal 123456789 50000`", parse_mode="Markdown")

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    game = data.get("game")
    player_id = data.get("player_id")
    package = data.get("package")
    user = message.from_user

    text = (
        f"🛒 **YANGI BUYURTMA! (FUNGO SHOP)**\n\n"
        f"👤 **Xaridor:** {user.first_name} (ID: `{user.id}`)\n"
        f"🎮 **O'yin:** {game}\n"
        f"🆔 **Player ID:** `{player_id}`\n"
        f"📦 **Paket:** {package}\n\n"
        f"📩 Username: @{user.username if user.username else 'Yo`q'}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Bajarildi", callback_data=f"done_{user.id}_{game}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_{user.id}")
        ]
    ])

    await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown", reply_markup=keyboard)
    await message.answer("✅ Buyurtmangiz qabul qilindi! Admin tez orada UC'ni hisobingizga o'tkazadi.")

@dp.callback_query(F.data.startswith("done_"))
async def order_done(callback: CallbackQuery):
    _, user_id, game = callback.data.split("_")
    try:
        await bot.send_message(
            chat_id=int(user_id), 
            text=f"🚀 Sizning **{game}** bo'yicha buyurtmangiz muvaffaqiyatli bajarildi! ✅"
        )
        await callback.message.edit_text(callback.message.text + "\n\n🟢 **STATUS: Bajarildi**")
    except Exception:
        pass

@dp.callback_query(F.data.startswith("cancel_"))
async def order_cancel(callback: CallbackQuery):
    _, user_id = callback.data.split("_")
    try:
        await bot.send_message(chat_id=int(user_id), text="❌ Buyurtmangiz bekor qilindi.")
        await callback.message.edit_text(callback.message.text + "\n\n🔴 **STATUS: Bekor qilindi**")
    except Exception:
        pass

# Render portini ochiq ushlab turish uchun mini veb-server
async def handle_ping(request):
    return web.Response(text="Bot is live!")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
