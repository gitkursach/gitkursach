#1819155073:AAGHK82SgrjwKk4BeYQwN7qiSaQTN7lleRA

# API ТЕЛЕГРАММА
import telebot
from telebot import types

import random
import os
import datetime
import time

# TOKEN
token = "1819155073:AAGHK82SgrjwKk4BeYQwN7qiSaQTN7lleRA"
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Создать новую БД.")
	item2 = types.KeyboardButton("Войти в существующую.")
	item3 = types.KeyboardButton("Забыл пароль")
	markup.add(item1)
	markup.add(item2)
	markup.add(item3)
	msg = bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}. Данный бот создан, что бы ты мог ничего не делать!<a href='https://yandex.ru/'>Ссылка на приложение</a>",
		parse_mode='html', reply_markup=markup)

# RUN
bot.polling(none_stop=True)
