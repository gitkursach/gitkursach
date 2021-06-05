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

# ХЕНДЛЕР НА СТАРТ
@bot.message_handler(commands=['start'])
def welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Создать новую БД.")
	item2 = types.KeyboardButton("Войти в существующую.")
	item3 = types.KeyboardButton("Забыл пароль")
	markup.add(item1, item2,item3)

	msg = bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}. Данный бот создан, что бы ты мог ничего не делать!<a href='https://yandex.ru/'>Ссылка на приложение</a>",
		parse_mode='html', reply_markup=markup)

	bot.register_next_step_handler(msg, func)



# ХЕНДЕЛЕР ХЗ НА ЧТО
@bot.message_handler(content_types=['text'])
def func(message):

	# ЧАТ ID КСТА
	chatId = message.chat.id
	
	if message.chat.type == 'private':
		# НУ ТИПО НОВУЮ БД СОЗДАЕМ
		if message.text == 'Создать новую БД.':

			user_name = ''
			user_mail = ''
			userID = ''

			def func_1(message):
				global user_name
				global userID
				user_name = message.text
				msg = bot.send_message(message.chat.id, 'Укажите ваше мыло: ')

				# УЗНАЕМ ID ТЕЛЕГРАММА НАШЕГО ЮЗЕРА
				userID = message.from_user.id

				bot.register_next_step_handler(msg, func_2)
			
			msg = bot.send_message(message.chat.id, 'Введите ФИО : ')
			bot.register_next_step_handler(msg, func_1)

			def func_2(message):
				global user_name
				global user_mail
				global userID
				user_mail = message.text
				msg = bot.send_message(message.chat.id, 'Ты указал свои данные, но в силу неподвласных мне причин, я не умею с ними ничего делать. Но вот они:')
				bot.send_message(message.chat.id, f'Твое имя: {user_name}')
				bot.send_message(message.chat.id, f'Твоя почта: {user_mail}')
				bot.send_message(message.chat.id, f'Твой ID: {userID}')





# RUN
bot.polling(none_stop=True)
