from traceback import print_tb
import telebot
from telebot import apihelper

apihelper.proxy = {'http':'socks4://A_korobeynikov:vfhn2022@10.5.95.99:3128'}

TOKEN='5238123062:AAG7hOcMjGbR6xoGTheEceJBhBP17bjQ2mM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.send_message(m.chat.id, 'Привет!' )

# bot.polling(timeout=1)

import requests
url = f"http://api.telegram.org/bot{TOKEN}/getMe"
req = requests.get(url, proxies={'http':'http://A_korobeynikov:vfhn2022@10.5.95.99:3128'})
print(req) 
print(req.status_code) 

