import telebot
import json
import os
from telebot import types

# Ambil token dari environment variable
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

files = {}
if os.path.exists("files.json"):
    with open("files.json", "r") as f:
        files = json.load(f)

@bot.message_handler(content_types=['document'])
def get_file_id(message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    files[file_name] = file_id

    with open("files.json", "w") as f:
        json.dump(files, f)

    bot.reply_to(message, f"✅ File '{file_name}' berhasil disimpan!\n🆔 ID: {file_id}")

@bot.message_handler(commands=['files'])
def show_files(message):
    if files:
        markup = types.InlineKeyboardMarkup()
        for i, file_name in enumerate(files.keys(), 1):
            button = types.InlineKeyboardButton(text=f"{i}. {file_name}", callback_data=f"send_{i}")
            markup.add(button)
        bot.reply_to(message, "📂 Pilih file untuk didownload:", reply_markup=markup)
    else:
        bot.reply_to(message, "❌ Belum ada file yang disimpan.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("send_"):
        nomor_file = int(call.data.split("send_")[1]) - 1
        file_name = list(files.keys())[nomor_file]
        if file_name in files:
            file_id = files[file_name]
            bot.send_document(call.message.chat.id, file_id, caption=f"📄 {file_name}")
        else:
            bot.send_message(call.message.chat.id, "❌ File tidak ditemukan.")

print("🤖 Bot is polling...")
bot.polling(none_stop=True)
