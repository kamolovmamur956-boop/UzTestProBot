import os
import telebot
from flask import Flask, request

BOT_TOKEN = "8942389214:AAFNWpNn18cxWfv-gxZkFi23f9EDqNHHXmU"
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
MATH_TESTS = [
    {"question": "1. 📐 Agar $2x + 5 = 15$ bo'lsa, $x$ ni toping.", "options": ["A) 3", "B) 4", "C) 5", "D) 6"], "answer": "C"},
    {"question": "2. 📈 Hisoblang: $3^3 + 2^4 - \\sqrt{49}$", "options": ["A) 34", "B) 36", "C) 40", "D) 43"], "answer": "A"},
    {"question": "3. 📉 120 kg uning $\\frac{3}{4}$ qismi sotildi. Necha kg qoldi?", "options": ["A) 20 kg", "B) 30 kg", "C) 40 kg", "D) 90 kg"], "answer": "B"},
    {"question": "4. 📐 Kvadrat yuzi $64 \\text{ cm}^2$, perimetrini toping.", "options": ["A) 16 cm", "B) 24 cm", "C) 32 cm", "D) 64 cm"], "answer": "C"},
    {"question": "5. 🔢 18 va 24 ning EKUKini toping.", "options": ["A) 48", "B) 72", "C) 96", "D) 144"], "answer": "B"},
    {"question": "6. ➗ $\\frac{x}{15} = \\frac{4}{5}$ proporsiyadan $x$ni toping.", "options": ["A) 10", "B) 12", "C) 15", "D) 20"], "answer": "B"},
    {"question": "7. 📊 20 ta o'quvchining o'rtacha yoshi 15. Yig'indini toping.", "options": ["A) 250", "B) 300", "C) 350", "D) 400"], "answer": "B"},
    {"question": "8. 📐 Katetlari 6 va 8 bo'lgan uchburchak gipotenuzasi?", "options": ["A) 9", "B) 10", "C) 12", "D) 14"], "answer": "B"},
    {"question": "9. 📉 400 ning 25 foizi nechaga teng?", "options": ["A) 50", "B) 75", "C) 100", "D) 125"], "answer": "C"},
    {"question": "10. 📐 $(x - 3)(x + 3) - x^2$ ni soddalashtiring.", "options": ["A) -9", "B) 9", "C) $2x^2$", "D) 0"], "answer": "A"}
]

user_progress = {}

@bot.message_handler(func=lambda message: message.text == "🧩 Majburiy Fanlar")
def select_mandatory_subject(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Matematika"),
        telebot.types.KeyboardButton("Tarix"),
        telebot.types.KeyboardButton("Ona tili")
    )
    markup.add(telebot.types.KeyboardButton("Asosiy menyu"))
    bot.send_message(message.chat.id, "Kerakli majburiy fanni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Matematika")
def start_math_test(message):
    chat_id = message.chat.id
    user_progress[chat_id] = {"index": 0, "score": 0, "subject": "math"}
    send_math_question(chat_id)

def send_math_question(chat_id):
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "math":
        return
    idx = data["index"]
    if idx < len(MATH_TESTS):
        q = MATH_TESTS[idx]
        markup = telebot.types.InlineKeyboardMarkup()
        for opt in q["options"]:
            markup.add(telebot.types.InlineKeyboardButton(opt, callback_data=f"ans_{opt[0]}"))
        bot.send_message(chat_id, q["question"], reply_markup=markup, parse_mode="Markdown")
    else:
        score = data["score"]
        bot.send_message(chat_id, f"🏆 Matematika testi yakunlandi!\nSizning natijangiz: {score}/10")
        user_progress.pop(chat_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ans_"))
def handle_math_answer(call):
    chat_id = call.message.chat.id
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "math":
        return
    selected = call.data.split("_")[1]
    idx = data["index"]
    if MATH_TESTS[idx]["answer"] == selected:
        data["score"] += 1
    data["index"] += 1
    bot.answer_callback_query(call.id, "Javob qabul qilindi!")
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    send_math_question(chat_id)
    HISTORY_TESTS = [
    {"question": "1. 🏛 Qadimgi Baqtriya davlati markazi qayerda joylashgan edi?", "options": ["A) Surxondaryo va Shimoliy Afg'oniston", "B) Farg'ona vodiysi", "C) Xorazm vohasi", "D) Zarafshon havzasi"], "answer": "A"},
    {"question": "2. 📜 Islom dini O'rta Osiyoda qaysi asrlardan boshlab keng tarqala boshladi?", "options": ["A) VII-VIII asrlar", "B) IX-X asrlar", "C) V-VI asrlar", "D) XI-XII asrlar"], "answer": "A"},
    {"question": "3. 👑 Sohibqiron Amir Temur qaysi yilda tavallud topgan?", "options": ["A) 1336-yil", "B) 1370-yil", "C) 1405-yil", "D) 1365-yil"], "answer": "A"},
    {"question": "4. 🌍 Buyuk Ipak yo'li dastlab qaysi ikki yirik hududni bog'lagan?", "options": ["A) Xitoy va Rim imperiyasi", "B) Hindiston va Misr", "C) Eron va Gretsiya", "D) Vizantiya va Xazar xoqonligi"], "answer": "A"},
    {"question": "5. 🏛 Xiva xonligini boshqargan sulolani aniqlang:", "options": ["A) Shayboniylar", "B) Ashtarxoniylar", "C) Anushteginiylar", "D) Mang'itlar"], "answer": "C"},
    {"question": "6. 📚 Mirzo Ulug'bek tomonidan Samarqandda astronomiya maktabi va observatoriya qurilgan yil?", "options": ["A) 1420-yil", "B) 1417-yil", "C) 1430-yil", "D) 1449-yil"], "answer": "A"},
    {"question": "7. ⚔️ Temuriylar davlatining poytaxti qaysi shahar bo'lgan?", "options": ["A) Buxoro", "B) Samarqand", "C) Toshkent", "D) Xiva"], "answer": "B"},
    {"question": "8. 📜 O'zbekiston Respublikasining ilk Konstitutsiyasi qachon qabul qilingan?", "options": ["A) 1991-yil 31-avgust", "B) 1992-yil 8-dekabr", "C) 1993-yil 2-iyul", "D) 1990-yil 24-mart"], "answer": "B"},
    {"question": "9. 🏛 Qo'qon xonligi mustaqil davlat sifatida qachon tashkil topgan?", "options": ["A) 1709-yil", "B) 1750-yil", "C) 1801-yil", "D) 1650-yil"], "answer": "A"},
    {"question": "10. 🔬 Al-Xorazmiy ilm-fanga qaysi yo'nalishda ulkan hissa qo'shgan?", "options": ["A) Fizika va Optika", "B) Algebra va Astronomiya", "C) Tibbiyot va Farmakologiya", "D) Kimyo va Mineralogiya"], "answer": "B"}
]

@bot.message_handler(func=lambda message: message.text == "Tarix")
def start_history_test(message):
    chat_id = message.chat.id
    user_progress[chat_id] = {"index": 0, "score": 0, "subject": "history"}
    send_history_question(chat_id)

def send_history_question(chat_id):
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "history":
        return
    idx = data["index"]
    if idx < len(HISTORY_TESTS):
        q = HISTORY_TESTS[idx]
        markup = telebot.types.InlineKeyboardMarkup()
        for opt in q["options"]:
            markup.add(telebot.types.InlineKeyboardButton(opt, callback_data=f"hist_{opt[0]}"))
        bot.send_message(chat_id, q["question"], reply_markup=markup, parse_mode="Markdown")
    else:
        score = data["score"]
        bot.send_message(chat_id, f"🏆 Tarix testi yakunlandi!\nSizning natijangiz: {score}/10")
        user_progress.pop(chat_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_"))
def handle_history_answer(call):
    chat_id = call.message.chat.id
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "history":
        return
    selected = call.data.split("_")[1]
    idx = data["index"]
    if HISTORY_TESTS[idx]["answer"] == selected:
        data["score"] += 1
    data["index"] += 1
    bot.answer_callback_query(call.id, "Javob qabul qilindi!")
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    send_history_question(chat_id)
    UZBEK_TESTS = [
    {"question": "1. 📚 Imlo jihatidan barcha so'zlar to'g'ri yozilgan qatorni aniqlang:", "options": ["A) Imkoniyat, sharoit, e'tibor", "B) Imkoniyat, sharoyit, e'tibor", "C) Imkoniyat, sharoit, eatibor", "D) Imkoniyat, sharoyit, etibor"], "answer": "A"},
    {"question": "2. ✍️ Tub so'zni aniqlang:", "options": ["A) Toshli", "B) Bilimdon", "C) Daraxt", "D) O'qituvchi"], "answer": "C"},
    {"question": "3. 🔤 O'zbek alifbosida nechta harf va nechta tovush bor?", "options": ["A) 28 ta harf, 32 ta tovush", "B) 29 ta harf, 30 ta tovush", "C) 29 ta harf, 31 ta tovush", "D) 26 ta harf, 29 ta tovush"], "answer": "B"},
    {"question": "4. 📌 Qaysi qatorda yasama so'z berilgan?", "options": ["A) Kitobxona", "B) Qalam", "C) Daftar", "D) Maktab"], "answer": "A"},
    {"question": "5. 🎯 Bosh kelishikdagi so'zni toping:", "options": ["A) Kitobni", "B) Kitobning", "C) Kitob", "D) Kitobda"], "answer": "C"},
    {"question": "6. 📝 Uyushiq bo'lakli gapni aniqlang:", "options": ["A) Kecha uyga bordim va dam oldim.", "B) Bog'da olma, o'rik, gilos pishdi.", "C) Quyosh chiqdi, havo isiydi.", "D) Men kitob o'qiyapman."], "answer": "B"},
    {"question": "7. 🔍 Ma'nodosh (sinonim) so'zlar qatorini ko'rsating:", "options": ["A) Katta — kichik", "B) Chiroyli — go'zal", "C) Issiq — sovuq", "D) Baland — past"], "answer": "B"},
    {"question": "8. 💡 Frazeologik birikmani toping:", "options": ["A) Qattiq yugurdi", "B) Yuziga soldi", "C) Baland ovozda gapirdi", "D) Kitob sotib oldi"], "answer": "B"},
    {"question": "9. 📖 Qaratqich kelishigining qo'shimchasini toping:", "options": ["A) -ni", "B) -ning", "C) -da", "D) -ga"], "answer": "B"},
    {"question": "10. ✍️ Orttirma nisbatdagi fe'lni aniqlang:", "options": ["A) Yozildi", "B) Yozdir", "C) Yozishdi", "D) Yozindi"], "answer": "B"}
]

@bot.message_handler(func=lambda message: message.text == "Ona tili")
def start_uzbek_test(message):
    chat_id = message.chat.id
    user_progress[chat_id] = {"index": 0, "score": 0, "subject": "uzbek"}
    send_uzbek_question(chat_id)

def send_uzbek_question(chat_id):
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "uzbek":
        return
    idx = data["index"]
    if idx < len(UZBEK_TESTS):
        q = UZBEK_TESTS[idx]
        markup = telebot.types.InlineKeyboardMarkup()
        for opt in q["options"]:
            markup.add(telebot.types.InlineKeyboardButton(opt, callback_data=f"uzb_{opt[0]}"))
        bot.send_message(chat_id, q["question"], reply_markup=markup, parse_mode="Markdown")
    else:
        score = data["score"]
        bot.send_message(chat_id, f"🏆 Ona tili testi yakunlandi!\nSizning natijangiz: {score}/10")
        user_progress.pop(chat_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("uzb_"))
def handle_uzbek_answer(call):
    chat_id = call.message.chat.id
    data = user_progress.get(chat_id)
    if not data or data.get("subject") != "uzbek":
        return
    selected = call.data.split("_")[1]
    idx = data["index"]
    if UZBEK_TESTS[idx]["answer"] == selected:
        data["score"] += 1
    data["index"] += 1
    bot.answer_callback_query(call.id, "Javob qabul qilindi!")
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    send_uzbek_question(chat_id)
    @bot.message_handler(func=lambda message: message.text in ["🧩 Majburiy Fanlar", "Majburiy Fanlar"])
def select_mandatory_subject(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Matematika"),
        telebot.types.KeyboardButton("Tarix"),
        telebot.types.KeyboardButton("Ona tili")
    )
    markup.add(telebot.types.KeyboardButton("Asosiy menyu"))
    bot.send_message(message.chat.id, "Kerakli majburiy fanni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🔙 Asosiy menyu", "Asosiy menyu"])
def back_to_main(message):
    send_welcome(message)
if __name__ == "__main__":
    RENDER_URL = "https://uztestprobot.onrender.com"
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

   
      
