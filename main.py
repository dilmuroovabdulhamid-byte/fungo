import os
import json
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8529363243:AAF6FeK5N8TVvv9YgaK7uM-RQUUgDi0uEHY"
ADMIN_ID = 5802084102

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "FUNGO SHOP Bot is active!"

@bot.message_handler(commands=['start'])
def start_command(message):
    # Inline WebApp tugmasini yaratish (sendData aynan shunday ochilganda ishlaydi)
    markup = InlineKeyboardMarkup()
    # GitHub Pages yoki hosting havolangizni shu yerga yozing
    web_app_url = "https://dilmuroovabdulhamid-byte.github.io/fungo/" 
    web_button = InlineKeyboardButton(text="🎮 Do'konni ochish", web_app=WebAppInfo(url=web_app_url))
    markup.add(web_button)

    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        f"🎮 **FUNGO SHOP** botiga xush kelibsiz.\n"
        f"O'yinlarga donat qilish uchun quyidagi tugmani bosing:",
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        
        game = data.get('game')
        player_id = data.get('player_id')
        package = data.get('package')
        
        user_name = message.from_user.first_name
        username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        user_id = message.from_user.id

        # 1. Mijozga to'lov rekvizitlarini yuborish
        user_msg = (
            f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
            f"🎮 **O'yin:** {game}\n"
            f"📦 **Paket:** {package}\n"
            f"🆔 **Player ID:** `{player_id}`\n\n"
            f"💳 **To'lov uchun karta raqami:**\n"
            f"`8600000000000000` (Karta egasi ismi)\n\n"
            f"⚠️ *To'lovni amalga oshirgach, chekni (skrinshotni) ushbu botga yuboring!*"
        )
        bot.send_message(message.chat.id, user_msg, parse_mode="Markdown")

        # 2. Adminga buyurtma haqida xabar yuborish
        try:
            admin_msg = (
                f"🛒 **YANGI BUYURTMA!**\n\n"
                f"👤 **Xaridor:** {user_name} ({username})\n"
                f"🆔 **User ID:** `{user_id}`\n"
                f"🎮 **O'yin:** {game}\n"
                f"📦 **Paket:** {package}\n"
                f"🔢 **Player ID:** `{player_id}`"
            )
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        except Exception as admin_err:
            print(f"Adminga yuborishda xatolik: {admin_err}")

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    user_id = message.from_user.id

    caption = (
        f"🧾 **YANGI TO'LOV CHEKI!**\n\n"
        f"👤 **Xaridor:** {user_name} ({username})\n"
        f"🆔 **User ID:** `{user_id}`"
    )

    try:
        if message.photo:
            photo_id = message.photo[-1].file_id
            bot.send_photo(ADMIN_ID, photo_id, caption=caption, parse_mode="Markdown")
        elif message.document:
            doc_id = message.document.file_id
            bot.send_document(ADMIN_ID, doc_id, caption=caption, parse_mode="Markdown")

        bot.send_message(message.chat.id, "✅ Chek qabul qilindi! Operator tez orada tekshirib, xizmatni bajaradi.")
    except Exception as e:
        print(f"Chek yuborishda xatolik: {e}")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
