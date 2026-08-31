import os
import telebot
from flask import Flask, request

BOT_TOKEN = "8942389214:AAFnWpnn18cxWfv-gxZkFi23f9EDqNhHXMw"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "UzTestProBot is running via Webhook!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid", 403

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🎯 Milliy Sertifikat")
    btn2 = telebot.types.KeyboardButton("🧩 Majburiy Fanlar")
    btn3 = telebot.types.KeyboardButton("⚛️ Mavzulashtirilgan Testlar")
    btn4 = telebot.types.KeyboardButton("🏆 Pedagogik Mahorat")
    btn5 = telebot.types.KeyboardButton("💳 Balans va Obuna")
    btn6 = telebot.types.KeyboardButton("📊 Mening natijalarim")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
    bot.send_message(
        message.chat.id,
        f"Salom, {message.from_user.first_name}! 🚀 UzTestPro botiga xush kelibsiz. Tayyorgarlik yo'nalishini tanlang:",
        reply_markup=markup
    )

if __name__ == "__main__":
    RENDER_URL = "https://uztestprobot.onrender.com"
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
