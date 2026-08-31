import telebot

BOT_TOKEN = "8942389214:AAFNWpNn18cxWfv-gxZkFi23f9EDqNHHXmU"
bot = telebot.TeleBot(BOT_TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🎯 Milliy Sertifikat")
    btn2 = telebot.types.KeyboardButton("📚 Majburiy Fanlar")
    btn3 = telebot.types.KeyboardButton("🧩 Mavzulashtirilgan Testlar")
    btn4 = telebot.types.KeyboardButton("👨‍🏫 Pedagogik Mahorat")
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

# Asosiy menyu xabarlari
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    
    if text == "🎯 Milliy Sertifikat":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton("⚛️ Fizika (30 talik test)", callback_data="ms_physics"),
            telebot.types.InlineKeyboardButton("📐 Matematika (30 talik test)", callback_data="ms_math")
        )
        bot.reply_to(message, "🎯 **Milliy Sertifikat** imtihoniga tayyorgarlik uchun fanni tanlang:", reply_markup=markup)
        
    elif text == "📚 Majburiy Fanlar":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton("📐 Majburiy Matematika", callback_data="maj_math"),
            telebot.types.InlineKeyboardButton("🇺🇿 Ona tili", callback_data="maj_uzbek"),
            telebot.types.InlineKeyboardButton("🇺🇿 O'zbekiston tarixi", callback_data="maj_history")
        )
        bot.reply_to(message, "📚 **Majburiy fanlar** bo'yicha testlar blokini tanlang:", reply_markup=markup)
        
    elif text == "🧩 Mavzulashtirilgan Testlar":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton("⚛️ Fizika (Mavzular bo'yicha)", callback_data="mav_physics"),
            telebot.types.InlineKeyboardButton("📐 Matematika (Mavzular bo'yicha)", callback_data="mav_math")
        )
        bot.reply_to(message, "🧩 Qaysi fan bo'yicha mavzulashtirilgan testlarni yechmoqchisiz?", reply_markup=markup)
        
    elif text == "👨‍🏫 Pedagogik Mahorat":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton(" pedagokika va psixologiya testlari", callback_data="ped_skill")
        )
        bot.reply_to(message, "👨‍🏫 O'qituvchilar uchun **Pedagogik mahorat va attestatsiya** testlari:", reply_markup=markup)
        
    elif text == "💳 Balans va Obuna":
        bot.reply_to(message, "💰 Sizning balansingiz: 0 so'm\n\nHisobni to'ldirish uchun tez orada to'lov tizimlari ulanadi.")
    elif text == "📊 Mening natijalarim":
        bot.reply_to(message, "📈 Sizning shaxsiy statistikangiz:\n• Yechilgan testlar soni: 0 ta\n• O'rtacha ko'rsatkich: 0%")
    else:
        bot.reply_to(message, "Iltimos, pastdagi tugmalardan birini tanlang yoki /start buyrug'ini bosing.")

# Inline tugmalar bosilganda ishlaydigan qism
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    bot.answer_callback_query(call.id)
    
    if data == "ms_physics":
        bot.send_message(call.message.chat.id, "⚛️ **Fizika Milliy Sertifikat (30 talik)** testi yuklanmoqda...\n\n(Bu yerda 30 ta tanlanma savol bazasi ishga tushadi)")
    elif data == "ms_math":
        bot.send_message(call.message.chat.id, "📐 **Matematika Milliy Sertifikat (30 talik)** testi yuklanmoqda...\n\n(Bu yerda 30 ta murakkab masalalar bazasi ishga tushadi)")
    elif data == "maj_math":
        bot.send_message(call.message.chat.id, "📐 Majburiy Matematika testlari tayyorlanmoqda...")
    elif data == "maj_uzbek":
        bot.send_message(call.message.chat.id, "🇺🇿 Ona tili testlari tayyorlanmoqda...")
    elif data == "maj_history":
        bot.send_message(call.message.chat.id, "🇺🇿 Tarix testlari tayyorlanmoqda...")
    elif data == "mav_physics":
        bot.send_message(call.message.chat.id, "⚛️ Fizika bo'yicha mavzular ro'yxati (Kinematika, Dinamika va h.k.) shakllantirilmoqda...")
    elif data == "mav_math":
        bot.send_message(call.message.chat.id, "📐 Matematika bo'yicha mavzular ro'yxati shakllantirilmoqda...")
    elif data == "ped_skill":
        bot.send_message(call.message.chat.id, "👨‍🏫 Pedagogik mahorat, zamonaviy pedagogik texnologiyalar va qonunchilik testlari yuklanmoqda...")

if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()