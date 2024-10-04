from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Файлы для хранения новостей, подписчиков и новостей на модерации
NEWS_FILE = "news.txt"
SUBSCRIBERS_FILE = "subscribers.txt"
PENDING_NEWS_FILE = "pending_news.txt"
PENDING_PHOTOS_DIR = "pending_photos"
NEWS_PHOTOS_DIR = "news_photos"

ADMIN_IDS = [7550293366]
MAX_NEWS_LENGTH = 500

if not os.path.exists(PENDING_PHOTOS_DIR):
    os.makedirs(PENDING_PHOTOS_DIR)
if not os.path.exists(NEWS_PHOTOS_DIR):
    os.makedirs(NEWS_PHOTOS_DIR)

def save_news(news_text):
    with open(NEWS_FILE, "a", encoding="utf-8") as file:
        file.write(news_text + "\n")

def save_pending_news(news_text, user_id):
    with open(PENDING_NEWS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{user_id}:{news_text}\n")

def get_pending_news():
    if not os.path.exists(PENDING_NEWS_FILE):
        return []
    with open(PENDING_NEWS_FILE, "r", encoding="utf-8") as file:
        pending_news = file.readlines()
    return pending_news

def remove_pending_news(index):
    pending_news = get_pending_news()
    if index < len(pending_news):
        del pending_news[index]
        with open(PENDING_NEWS_FILE, "w", encoding="utf-8") as file:
            file.writelines(pending_news)

def add_subscriber(user_id):
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as file:
            file.write(str(user_id) + "\n")
    else:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
            subscribers = file.readlines()

        if str(user_id) + "\n" not in subscribers:
            with open(SUBSCRIBERS_FILE, "a", encoding="utf-8") as file:
                file.write(str(user_id) + "\n")

def remove_subscriber(user_id):
    if not os.path.exists(SUBSCRIBERS_FILE):
        return
    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
        subscribers = file.readlines()
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as file:
        for subscriber in subscribers:
            if str(user_id) + "\n" != subscriber:
                file.write(subscriber)

def get_all_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
        subscribers = file.readlines()
    return [int(sub.strip()) for sub in subscribers]

def get_all_news():
    if not os.path.exists(NEWS_FILE):
        return "Новостей пока нет."
    with open(NEWS_FILE, "r", encoding="utf-8") as file:
        news = file.readlines()
    if not news:
        return "Новостей пока нет."
    return "".join(news)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Последние новости", callback_data='get_news')],
        [InlineKeyboardButton("Отправить новость", callback_data='send_news')],
        [InlineKeyboardButton("Подписаться на рассылку новостей", callback_data='subscribe')],
        [InlineKeyboardButton("Отписаться от новостей", callback_data='unsubscribe')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

async def handle_news_submission(update: Update, context: CallbackContext):
    # Обработка новостей
    pass

updater = Updater("7550293366:AAH4kq9-Yfr2NHGkC30HwIMoyVC4lXBlaNI", use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_news_submission))

updater.start_polling()
updater.idle()
