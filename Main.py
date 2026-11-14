import os
import json
import random
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), BaseHTTPRequestHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

keep_alive()
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

try:
    with open("collection.json", "r", encoding="utf-8") as f:
        COLLECTION = json.load(f)
except:
    COLLECTION = []

count = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is now ONLINE! Keep chatting in the group and photos will appear.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    count[chat_id] = count.get(chat_id, 0) + 1
    if count[chat_id] >= 8:
        count[chat_id] = 0
        if COLLECTION:
            item = random.choice(COLLECTION)
            try:
                await update.message.reply_photo(photo=item["photo"], caption=item.get("caption", ""))
            except:
                await update.message.reply_text(item.get("caption", ""))
        else:
            await update.message.reply_text("Collection is empty!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
