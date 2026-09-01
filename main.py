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

if __name__ == "__main__":
    RENDER_URL = "https://uztestprobot.onrender.com"
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# Matematika fanidan testlar bazasi (10 ta namuna)
MATH_TESTS = [
    {
        "question": "1. 📐 Agar $2x + 5 = 15$ bo'lsa, $x$ ning qiymatini toping.",
        "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
        "answer": "C"
    },
    {
        "question": "2. 📈 Hisoblang: $3^3 + 2^4 - \\sqrt{49}$",
        "options": ["A) 34", "B) 36", "C) 40", "D) 43"],
        "answer": "A"
    },
    {
        "question": "3. 📉 Do'konda 120 kg un bor edi. Uning $\\frac{3}{4}$ qismi sotildi. Necha kg un qoldi?",
        "options": ["A) 20 kg", "B) 30 kg", "C) 40 kg", "D) 90 kg"],
        "answer": "B"
    },
    {
        "question": "4. 📐 Kvadratning yuzi $64 \\text{ cm}^2$ bo'lsa, uning perimetrini toping.",
        "options": ["A) 16 cm", "B) 24 cm", "C) 32 cm", "D) 64 cm"],
        "answer": "C"
    },
    {
        "question": "5. 🔢 18 va 24 sonlarining eng kichik umumiy karralisini (EKUK) toping.",
        "options": ["A) 48", "B) 72", "C) 96", "D) 144"],
        "answer": "B"
    },
    {
        "question": "6. ➗ Proporsiyaning noma'lum hadini toping: $\\frac{x}{15} = \\frac{4}{5}$",
        "options": ["A) 10", "B) 12", "C) 15", "D) 20"],
        "answer": "B"
    },
    {
        "question": "7. 📊 Jamoadagi 20 ta o'quvchining o'rtacha yoshi 15 yosh. Ularning yoshlari yig'indisini toping.",
        "options": ["A) 250", "B) 300", "C) 350", "D) 400"],
        "answer": "B"
    },
    {
        "question": "8. 📐 To'g'ri burchakli uchburchakning katetlari 6 cm va 8 cm bo'lsa, gipotenuzasini toping.",
        "options": ["A) 9 cm", "B) 10 cm", "C) 12 cm", "D) 14 cm"],
        "answer": "B"
    },
    {
        "question": "9. 📉 400 sonining 25 foizini toping.",
        "options": ["A) 50", "B) 75", "C) 100", "D) 125"],
        "answer": "C"
    },
    {
        "question": "10. 📐 Ifodani soddalashtiring: $(x - 3)(x + 3) - x^2$",
        "options": ["A) -9", "B) 9", "C) $2x^2 - 9$", "D) 0"],
        "answer": "A"
    }
]

# Foydalanuvchilarning testdagi jarayonini saqlash uchun
user_progress = {}

@bot.message_handler(func=lambda message: message.text == "🧩 Majburiy Fanlar" or message.text == "📐 Matematikadan test")
def start_math_test(message):
    chat_id = message.chat.id
    user_progress[chat_id] = {"index": 0, "score": 0}
    send_math_question(chat_id)

def send_math_question(chat_id):
    data = user_progress.get(chat_id)
    if not data:
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
        bot.send_message(chat_id, f"🏆 Test yakunlandi!\nSizning natijangiz: {score}/10")
        user_progress.pop(chat_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ans_"))
def handle_math_answer(call):
    chat_id = call.message.chat.id
    data = user_progress.get(chat_id)
    if not data:
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
    # Tarix fanidan testlar bazasi (10 ta namuna)
HISTORY_TESTS = [
    {
        "question": "1. 🏛 Qadimgi Baqtriya davlati qaysi hozirgi hududda joylashgan edi?",
        "options": ["A) Surxondaryo va Shimoliy Afg'oniston", "B) Farg'ona vodiysi", "C) Xorazm vohasi", "D) Zarafshon vodiysi"],
        "answer": "A"
    },
    {
        "question": "2. 📜 O'rta osiyoda qaysi asrda Islom dini tarqala boshladi?",
        "options": ["A) VII-VIII asrlar", "B) IX-X asrlar", "C) V-VI asrlar", "D) XI-XII asrlar"],
        "answer": "A"
    },
    {
        "question": "3. 👑 Amir Temur qaysi yilda tavallud topgan?",
        "options": ["A) 1336-yil", "B) 1370-yil", "C) 1405-yil", "D) 1365-yil"],
        "answer": "A"
    },
    {
        "question": "4. 🌍 Buyuk Ipak yo'li qaysi qit'alarni bog'lagan?",
        "options": ["A) Yevropa va Amerika", "B) Osiyo va Yevropa", "C) Afrika va Avstraliya", "D) Osiyo va Afrika"],
        "answer": "B"
    },
    {
        "question": "5. 🏛 Xiva xonligiga asos solgan sulola vakili kim?",
        "options": ["A) Shayboniylar", "B) Ashtarxoniylar", "C) Anushteginiylar (Shayboniylar tarmog'i)", "D) Mang'itlar"],
        "answer": "C"
    },
    {
        "question": "6. 📚 Mirzo Ulug'bek tomonidan Samarqandda qachon observatoriya qurilgan?",
        "options": ["A) 1420-yil", "B) 1417-yil", "C) 1430-yil", "D) 1449-yil"],
        "answer": "A"
    },
    {
        "question": "7. ⚔️ Temuriylar davlati poytaxti qaysi shahar bo'lgan?",
        "options": ["A) Buxoro", "B) Samarqand", "C) Toshkent", "D) Xiva"],
        "answer": "B"
    },
    {
        "question": "8. 📜 O'zbekiston Respublikasining Konstitutsiyasi qachon qabul qilingan?",
        "options": ["A) 1991-yil 31-avgust", "B) 1992-yil 8-dekabr", "C) 1993-yil 2-mart", "D) 1989-yil 21-oktabr"],
        "answer": "B"
    },
    {
        "question": "9. 🏛 Qo'qon xonligi qaysi yilda tashkil topgan?",
        "options": ["A) 1709-yil", "B) 1750-yil", "C) 1801-yil", "D) 1650-yil"],
        "answer": "A"
    },
    {
        "question": "10. 🔬 Al-Xorazmiy qaysi fan rivojiga ulkan hissa qo'shgan?",
        "options": ["A) Fizika", "B) Algebra (Matematika) va Astronomiya", "C) Tibbiyot", "D) Kimyo"],
        "answer": "B"
    }
]

# Tarix testi uchun boshqaruv funksiyasi
@bot.message_handler(func=lambda message: message.text == "📜 Tarixiy Testlar" or message.text == "🇺🇿 Tarix")
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
        bot.send_message(chat_id, f"🏆 Tarix test yakunlandi!\nSizning natijangiz: {score}/10")
        user_progress.pop(chat_id, None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_"))
def handle_history_answer(call):
    chat_id = call.message.chat.id
    data = user_progress.get(chat_id)
    if not data:
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
    # Ona tili fanidan testlar bazasi (10 ta namuna)
UZBEK_TESTS = [
    {
        "question": "1. 📚 Qaysi qatordagi barcha so'zlar imlo jihatidan to'g'ri yozilgan?",
        "options": ["A) Imkoniyat, sharoit, e'tibor", "B) Imkoniyat, sharoyit, e'tibor", "C) Imkoniyat, sharoit, eatibor", "D) Imkoniyat, sharoit, etibor"],
        "answer": "A"
    },
    {
        "question": "2. ✍️ Tub so'zni aniqlang:",
        "options": ["A) Toshli", "B) Bilimdon", "C) Daraxt", "D) O'qituvchi"],
        "answer": "C"
    },
    {
        "question": "3. 🔤 O'zbek alifbosida nechta harf va nechta tovush bor?",
        "options": ["A) 28 ta harf, 32 ta tovush", "B) 29 ta harf, 30 ta tovush", "C) 29 ta harf, 31 ta tovush", "D) 26 ta harf, 29 ta tovush"],
        "answer": "B"
    },
    {
        "question": "4. 📌 Qaysi qatorda yasama so'z berilgan?",
        "options": ["A) Kitobxona", "B) Qalam", "C) Daftar", "D) Maktab"],
        "answer": "A"
    },
    {
        "question": "5. 🎯 Bosh kelishikdagi so'zni toping:",
        "options": ["A) Kitobni", "B) Kitobning", "C) Kitob", "D) Kitobda"],
        "answer": "C"
    },
    {
        "question": "6. 📝 Uyushiq bo'lakli gapni aniqlang:",
        "options": ["A) Kecha uyga bordim va dam oldim.", "B) Bog'da olma, o'rik, gilos pishdi.", "C) Quyosh chiqdi, havo isiydi.", "D) Men kitob o'qiyapman."],
        "answer": "B"
    },
    {
        "question": "7. 🔍 Ma'nodosh (sinonim) so'zlar qatorini ko'rsating:",
        "options": ["A) Katta — kichik", "B) Chiroyli — go'zal", "C) Issiq — sovuq", "D) Baland — past"],
        "answer": "B"
    },
    {
        "question": "8. 💡 Frazeologik birikmani toping:",
        "options": ["A) Qattiq yugurdi", "B) Yuziga soldi", "C) Baland ovozda gapirdi", "D) Kitob sotib oldi"],
        "answer": "B"
    },
    {
        "question": "9. 📖 Qaratqich kelishigining qo'shimchasini toping:",
        "options": ["A) -ni", "B) -ning", "C) -da", "D) -ga"],
        "answer": "B"
    },
    {
        "question": "10. ✍️ Orttirma nisbatdagi fe'lni aniqlang:",
        "options": ["A) Yozildi", "B) Yozdir", "C) Yozishdi", "D) Yozindi"],
        "answer": "B"
    }
]

# Ona tili testi uchun boshqaruv funksiyasi
@bot.message_handler(func=lambda message: message.text == "🇺🇿 Ona tili" or message.text == "📖 Ona tili Testlari")
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
    if not data:
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
