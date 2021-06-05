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

def add_more_room(cmci):
	global room
	global floor
	def add_floor(message):
		floor = message.text
		msg = bot.send_message(cmci, f'Введите номер кабинета : ')
		bot.register_next_step_handler(msg, add_room) 

	def add_room(message):

		room = message.text

		bot.send_message(cmci, f'Кабинет добавлен:')

		markup = types.InlineKeyboardMarkup(row_width = 1)
		item1 = types.InlineKeyboardButton("Да", callback_data = 'add_person')
		item2 = types.InlineKeyboardButton("Нет (Выйти в меню)", callback_data = 'leave')
		markup.add(item1, item2)
		bot.send_message(cmci, f"Этаж №{'floor'} Кабинет №{'room'} Добавляем сотрудника?",
		parse_mode='html', reply_markup=markup)


		
	msg = bot.send_message(cmci, 'Добавляем кабинет. Введите этаж :')
	bot.register_next_step_handler(msg, add_floor) 	



def mainmenu():
	markup = types.InlineKeyboardMarkup(row_width = 1)
	item1 = types.InlineKeyboardButton("Создать новую БД.", callback_data = 'create')
	item2 = types.InlineKeyboardButton("Войти в существующую.", callback_data = 'login')
	item3 = types.InlineKeyboardButton("Забыл пароль", callback_data = 'repair')
	markup.add(item1, item2,item3)
	return markup

@bot.message_handler(commands=['start'])
def welcome(message):
	markup = types.InlineKeyboardMarkup(row_width = 1)
	item1 = types.InlineKeyboardButton("Создать новую БД.", callback_data = 'create')
	item2 = types.InlineKeyboardButton("Войти в существующую.", callback_data = 'login')
	item3 = types.InlineKeyboardButton("Забыл пароль", callback_data = 'repair')
	markup.add(item1, item2,item3)

	bot.send_message(message.chat.id, "Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!",
	parse_mode='html', reply_markup=markup)



# ХЕНДЕЛЕР ХЗ НА ЧТО
@bot.callback_query_handler(func = lambda call: True)
def func(call):
	user_name = ''
	user_mail = ''
	userID = ''
	room = ''
	floor = ''
	brench_num = ''
	brench_adress = ''

	if call.message:
		if call.data == 'create':
			# ЧАТ ID КСТА
			chatId = call.message.chat.id
			# УЗНАЕМ ID ТЕЛЕГРАММА НАШЕГО ЮЗЕРА
			def func_1(message):
				global user_name
				user_name = message.text
				msg = bot.send_message(call.message.chat.id, 'Укажите ваше мыло: ')
				bot.register_next_step_handler(msg, func_2)
			def func_2(message):
				global user_name
				global user_mail
				global userID
				user_mail = message.text
				msg = bot.send_message(call.message.chat.id, 'Ты указал свои данные, но в силу неподвласных мне причин, я не умею с ними ничего делать. Но вот они:')
				bot.send_message(call.message.chat.id, f'Твое имя: {user_name}')
				bot.send_message(call.message.chat.id, f'Твоя почта: {user_mail}')
				bot.send_message(call.message.chat.id, f'Твой ID: {call.message.from_user.id}')

				markup = types.InlineKeyboardMarkup(row_width = 1)
				item1 = types.InlineKeyboardButton("Добавить отдел", callback_data = 'add')
				item2 = types.InlineKeyboardButton("Назад", callback_data = 'back')
				markup.add(item1, item2)	

				bot.send_message(message.chat.id, f"Что дальше? {call.data}",
				parse_mode='html', reply_markup=markup)
				print(call.data)

			msg = bot.send_message(call.message.chat.id, 'Введите ФИО : ')
			bot.register_next_step_handler(msg, func_1)
		if call.data == 'back':
			print(call.data)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
			text='Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!', reply_markup=mainmenu())
		if call.data == 'add':
			print(call.data)
			markup = types.InlineKeyboardMarkup(row_width = 1)
			item1 = types.InlineKeyboardButton("Да (добавить)", callback_data = 'yes')
			item2 = types.InlineKeyboardButton("Нет (пропустить этап)", callback_data = 'no')
			markup.add(item1, item2)	

			bot.send_message(call.message.chat.id, f"У вас есть филиалы?",
			parse_mode='html', reply_markup=markup)
			print(call.data)

		if call.data == 'no':
			add_more_room(call.message.chat.id)

		if call.data == 'yes':

			def add_brench_num(message):
				global brench_num
				brench_num = message.text
				msg = bot.send_message(call.message.chat.id, f'Введите адрес : ')
				bot.register_next_step_handler(msg, add_brench_adress) 

			def add_brench_adress(message):
				global room
				global floor
				global brench_num
				global brench_adress
				brench_adress = message.text
				bot.send_message(call.message.chat.id, f'филиал добавлен:')
				bot.send_message(call.message.chat.id, f'Номер : {brench_num}')
				bot.send_message(call.message.chat.id, f'Адрес : {brench_adress}')
				add_more_room(call.message.chat.id)



			msg = bot.send_message(call.message.chat.id, 'Добавляем филиал. Введите номер : ')
			bot.register_next_step_handler(msg, add_brench_num) 

		






#@bot.callback_query_handler(func = lambda call: True)
#def func_branch(call):
#	if call.message:
#		if call.data == "back":
#			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
#			text='Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!', reply_markup=mainmenu())	


# RUN
bot.polling(none_stop=True)