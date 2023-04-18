import os
import json
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bem-vindo, eu sou um robô assistente na Balaio Rural!")

def show_catalog(update: Update, context: CallbackContext):
    with open('catalog.json', 'r') as f:
        catalog = json.load(f)

    message = "Aqui está o catálogo de listas de compras coletivas:\n\n"

    for item in catalog:
        message += f"{item['title']} - R$ {item['price']} - /item{item['id']}\n"

    update.message.reply_text(message)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    item_id = int(query.data[4:])

    with open('catalog.json', 'r') as f:
        catalog = json.load(f)

    item = next((i for i in catalog if i['id'] == item_id), None)

    if item:
        message = f"{item['title']}\n\n{item['description']}\n\nPreço: R$ {item['price']}\n\n[image: {item['image_url']}]"
        query.edit_message_text(message)
    else:
        query.answer("Item não encontrado.")

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    with open('patterns.json', 'r') as f:
        patterns = json.load(f)

    for pattern in patterns:
        regex = re.compile(pattern['pattern'], re.IGNORECASE | re.UNICODE)
        if regex.match(user_message):
            update.message.reply_text(pattern['response'])
            return

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("catalogo", show_catalog))
dp.add_handler(CallbackQueryHandler(handle_callback))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
