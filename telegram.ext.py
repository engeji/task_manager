from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

TOKEN='5238123062:AAG7hOcMjGbR6xoGTheEceJBhBP17bjQ2mM'
REQUEST_KWARGS={
    'proxy_url': 'http://A_korobeynikov:vfhn2022@10.5.95.99:3128',
}
updater = Updater(TOKEN, use_context=TRUE, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
