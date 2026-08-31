import telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = "8942389214:AAFnWpnn18cxWfv-gxZkFi23f9EDqNhHXMw"
bot = telebot.TeleBot(BOT_TOKEN)

# Render port muammosini hal qilish uchun Flask veb-server
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# /start buyrug'i
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
    keep_alive()  # Veb-serverni ishga tushiradi
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
