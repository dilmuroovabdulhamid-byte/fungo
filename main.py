import json

# Sizning Telegram ID raqamingiz
ADMIN_ID = 5802084102  

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        # Mini App'dan kelgan buyurtma ma'lumotlarini o'qish
        data = json.loads(message.web_app_data.data)
        
        game = data.get('game')
        player_id = data.get('player_id')
        package = data.get('package')
        
        user_name = message.from_user.first_name
        username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        user_id = message.from_user.id

        # 1. Xaridorning o'ziga to'lov rekvizitlarini yuborish
        user_msg = (
            f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
            f"🎮 **O'yin:** {game}\n"
            f"📦 **Paket:** {package}\n"
            f"🆔 **Player ID:** `{player_id}`\n\n"
            f"💳 **To'lov uchun karta raqami:**\n"
            f"`8600000000000000` (Karta egasi ismi)\n\n"
            f"⚠️ *To'lovni amalga oshirgach, chekni (skrinshotni) shu botga yuboring!*"
        )
        bot.send_message(message.chat.id, user_msg, parse_mode="Markdown")

        # 2. Sizning shaxsiy Telegramingizga (ADMIN_ID) buyurtmani yuborish
        admin_msg = (
            f"🛒 **YANGI BUYURTMA!**\n\n"
            f"👤 **Xaridor:** {user_name} ({username})\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"🎮 **O'yin:** {game}\n"
            f"📦 **Paket:** {package}\n"
            f"🔢 **Player ID:** `{player_id}`"
        )
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
