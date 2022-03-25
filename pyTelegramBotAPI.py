from ctypes import resize
from traceback import print_tb
import telebot
from telebot import types
# from telebot import apihelper

# apihelper.proxy = {'http':'socks4://A_korobeynikov:vfhn2022@10.5.95.99:3128'}

TOKEN='5238123062:AAG7hOcMjGbR6xoGTheEceJBhBP17bjQ2mM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.send_message(m.chat.id, 'женялох!' )

@bot.message_handler(commands=['button'])
def button_message(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Кнопка')
    markup.add(item1)
    bot.send_message(m.chat.id, 'press button', reply_markup=markup)

bot.infinity_polling()



