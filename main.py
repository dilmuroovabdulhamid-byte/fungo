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
    user_name = message.from_user.first_name

    # Matn ostidagi Inline tugma (Mini App)
    markup = InlineKeyboardMarkup()
    web_app_url = "https://dilmuroovabdulhamid-byte.github.io/fungo/"
    app_button = InlineKeyboardButton(text="🚀 Ilovaga kirish", web_app=WebAppInfo(url=web_app_url))
    markup.add(app_button)

    # Siz so'ragan matn ko'rinishi
    caption = (
        f"Assalomu alaykum, {user_name}!\n\n"
        f"🎮 **FUNGO SHOP** botiga xush kelibsiz.\n"
        f"O'yinlarga donat qilish uchun quyidagi tugmani bosing:"
    )

    bot.send_message(
        message.chat.id, 
        caption, 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
