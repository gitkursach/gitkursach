# 1819155073:AAGHK82SgrjwKk4BeYQwN7qiSaQTN7lleRA

# API ТЕЛЕГРАММА
import telebot
from telebot import types

import random
import os
import datetime
import time
# postgresql
import psycopg2
from psycopg2 import Error

# TOKEN
token = "1819155073:AAGQsLiHM1y6omMJYdldIhGiJrfSN7SHL4g"
bot = telebot.TeleBot(token)


# ЧИСТКА СООБЩЕНИЙ ЗА ЮЗЕРОМ
# def messageClear(chatId, messageId):
#	bot.delete_message(chatId, messageId)


# ДОБАВЛЕНИЕ СОТРУДНИКОВ

def finishWorkers(chatId):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Да (Добавть ещё одного)", callback_data='yesAddPerson')
    item2 = types.InlineKeyboardButton("Закончить (Перейти к работе с БД)", callback_data='end')
    item3 = types.InlineKeyboardButton("Забыл пароль", callback_data='recover')
    markup.add(item1, item2)

    bot.send_message(chatId, "Сотрудник добавлен. Добавляем ещё?",
                     parse_mode='html', reply_markup=markup)


def haveSubWorkers(chatId):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Да (Позволит ему самостоятельно добавлять подченённых в БД)",
                                       callback_data='yesSubWorkers')
    item2 = types.InlineKeyboardButton("Нет (Запретит ему данную функцию)", callback_data='noSubWorkers')
    markup.add(item1, item2)

    msg = bot.send_message(chatId, "Разрешить ли ему добавлять подченённых? ",
                           parse_mode='html', reply_markup=markup)


def add_persons(chatId):
    def workWithClients(message):
        AddStaffDepart.append(message.text)
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Да (Позволит обрабатывать обращения клиентов)", callback_data='yesWork')
        item2 = types.InlineKeyboardButton("Нет (Запретит ему доступ к клиентам)", callback_data='noWork')
        markup.add(item1, item2)

        msg = bot.send_message(chatId, "Разрешить ли ему работать с клиентами?",
                               parse_mode='html', reply_markup=markup)

    def email(message):
        AddStaffDepart.append(message.text)
        msg = bot.send_message(chatId, "Введите его почту : ",
                               parse_mode='html')
        bot.register_next_step_handler(msg, workWithClients)

    msg = bot.send_message(chatId, "Добавляем Сотрудника. Введите его ФИО : ",
                           parse_mode='html')
    bot.register_next_step_handler(msg, email)


# ДОБАВЛЕНИЕ ПОДЧЕНЁННЫХ

def subFinish(chatId):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Да (Добавть ещё одного)", callback_data='subYesAddPerson')
    item2 = types.InlineKeyboardButton("Закончить (Выйти в меню)", callback_data='subEnd')
    markup.add(item1, item2)

    bot.send_message(chatId, "Сотрудник добавлен. Добавляем ещё?",
                     parse_mode='html', reply_markup=markup)


def subHaveSubWorkers(chatId):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Да (Позволит работнику добавлять подченённых)", callback_data='sub1YesWork')
    item2 = types.InlineKeyboardButton("Нет (Запретит ему добавление)", callback_data='sub1NoWork')
    markup.add(item1, item2)

    msg = bot.send_message(chatId, "Разрешить ли ему добалять подченённых?",
                           parse_mode='html', reply_markup=markup)


def subAdd_person(chatId):
    def subWorkWithClients(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Да (Позволит обрабатывать обращения клиентов)", callback_data='subYesWork')
        item2 = types.InlineKeyboardButton("Нет (Запретит ему доступ к клиентам)", callback_data='subNoWork')
        markup.add(item1, item2)

        msg = bot.send_message(chatId, "Разрешить ли ему работать с клиентами?",
                               parse_mode='html', reply_markup=markup)

    def subEmail(message):
        msg = bot.send_message(chatId, "Введите его EMAIL : ",
                               parse_mode='html')
        bot.register_next_step_handler(msg, subWorkWithClients)

    msg = bot.send_message(chatId, "Добавляем подчинённых. Введите его ФИО : ",
                           parse_mode='html')
    bot.register_next_step_handler(msg, subEmail)


# ДОБАВЛЕНИЕ КОМНАТ
def add_rooms(call):
    global AddDepart
    AddDepart = []
    global AddStaffDepart
    AddStaffDepart = []

    def addDepartToBD(AddDepart):
        try:
            print(AddDepart)
            DepartNumber = AddDepart[0]
            DepartCabinet = AddDepart[1]
            # DepartName = AddStaffDepart[0]
            # DepartBranch = AddStaffDepart[1]
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="123",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="BOT")

            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # Распечатать сведения о PostgreSQL
            print("Информация о сервере PostgreSQL")
            print(connection.get_dsn_parameters(), "\n")
            # Выполнение SQL-запроса

            Telegram_id = call.from_user.id
            cursor.execute(
                f"INSERT INTO \"Department\"  (\"DepartNumber\", \"DepartCabinet\", \"Telegram_id\") VALUES('{DepartNumber}', '{DepartCabinet}', '{Telegram_id}');")
            connection.commit()
            cursor.execute(f"SELECT \"department_id\" FROM  \"Department\" WHERE \"Telegram_id\" = '{Telegram_id}'")
            department_id = int(cursor.fetchall()[-1])
            print(department_id)
            # cursor.execute(
            #          f"UPDATE \"Department\" SET \"DepartName\" = {DepartName} AND \"DepartBranch\" = {DepartBranch} WHERE department_id = {department_id}")
            # connection.commit()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")



    def cab_number(message):
        AddDepart.append(message.text)
        msg = bot.send_message(call.message.chat.id, "Введите номер кабинета : ",
                               parse_mode='html')
        bot.register_next_step_handler(msg, finish)

    def finish(message):
        AddDepart.append(message.text)
        addDepartToBD(AddDepart)
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Да (Добавть ещё один кабинет)", callback_data='yesAddCab')
        item2 = types.InlineKeyboardButton("Нет (Перейти к добавлению сотрудников)", callback_data='noNext')
        item3 = types.InlineKeyboardButton("Забыл пароль", callback_data='recover')
        markup.add(item1, item2)

        bot.send_message(message.chat.id, "Кабинет добавлен. Добавляем ещё?",
                         parse_mode='html', reply_markup=markup)

    msg = bot.send_message(call.message.chat.id, "Добавляем кабинет. Введите его этаж : ",
                           parse_mode='html')
    bot.register_next_step_handler(msg, cab_number)


# ВЫВОД МЕНЮ
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Создать новую БД.", callback_data='create')
    item2 = types.InlineKeyboardButton("Войти в существующую.", callback_data='login')
    item3 = types.InlineKeyboardButton("Забыл пароль", callback_data='repair')
    markup.add(item1, item2, item3)
    return markup


# ВЫВОД МЕНЮ БАЗЫ
def db_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Управление подченёнными", callback_data='subWorkersControle')
    item2 = types.InlineKeyboardButton("Список корпоративных паролей", callback_data='passList')
    item3 = types.InlineKeyboardButton("Список Клиентов", callback_data='clientsList')
    item4 = types.InlineKeyboardButton("Добавить подчинённого", callback_data='addSubWorker')
    item5 = types.InlineKeyboardButton("На главную", callback_data='back')
    markup.add(item1, item2, item3, item4, item5)
    return markup


# НАЧАЛО
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Создать новую БД.", callback_data='create')
    item2 = types.InlineKeyboardButton("Войти в существующую.", callback_data='login')
    item3 = types.InlineKeyboardButton("Забыл пароль", callback_data='recover')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!",
                     parse_mode='html', reply_markup=markup)


# ОТЛОВ ВАРИАНТОВ
@bot.callback_query_handler(func=lambda call: True)
def catch(call):
    global currentMessage
    global AddPersanalData
    AddPersanalData = []

    if call.message:

        # СОЗДАНИЕ НОВОЙ БД (callback_data = create)
        if call.data == 'create':
            def addbdpersonal(AddPersanalData):
                try:
                    print(AddPersanalData)
                    FIO = AddPersanalData[0]
                    Phone = AddPersanalData[1]
                    Mail = AddPersanalData[2]
                    # Подключение к существующей базе данных
                    connection = psycopg2.connect(user="postgres",
                                                  # пароль, который указали при установке PostgreSQL
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="BOT")

                    # Курсор для выполнения операций с базой данных
                    cursor = connection.cursor()
                    # Распечатать сведения о PostgreSQL
                    print("Информация о сервере PostgreSQL")
                    print(connection.get_dsn_parameters(), "\n")
                    # Выполнение SQL-запроса

                    Telegram_id = call.from_user.id
                    cursor.execute(
                        f"INSERT INTO \"PersonalData\"  (\"FIO\", \"Mail\", \"Telegram_id\", \"Phone\") VALUES('{FIO}', '{Mail}', '{Telegram_id}', '{Phone}');")
                    connection.commit()

                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("Соединение с PostgreSQL закрыто")

            def Phone(message):

                AddPersanalData.append(message.text)
                msg = bot.send_message(call.message.chat.id, f'Введите Phone : ')
                bot.register_next_step_handler(msg, email)

            def email(message):

                AddPersanalData.append(message.text)

                msg = bot.send_message(call.message.chat.id, f'Введите EMAIL : ')
                bot.register_next_step_handler(msg, finish)

            def finish(message):

                AddPersanalData.append(message.text)
                addbdpersonal(AddPersanalData)
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Добавить отдел", callback_data='add_branch')
                item2 = types.InlineKeyboardButton("Назад (в меню)", callback_data='back')
                markup.add(item1, item2)
                bot.send_message(message.chat.id,
                                 "Ты указал свои данные, но в силу неподвласных мне причин, я не умею с ними ничего делать.",
                                 parse_mode='html', reply_markup=markup)

            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, f'Введите ФИО :')

            bot.register_next_step_handler(msg, Phone)

        # ВОЗВРАЩЕНИЕ В МЕНЮ ИЗ ЛЮБОЙ ТОЧКИ БОТА (ГДЕ ЭТО ВОЗМОЖНО) (callback_data = back)
        if call.data == 'back':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!',
                                  reply_markup=main_menu())

        # ДОБАВЛЕНИЕ ОТДЕЛА (callback_data = add_branch)
        if call.data == 'add_branch':
            bot.delete_message(call.message.chat.id, call.message.message_id)

            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Да (добавить)", callback_data='yesAdd')
            item2 = types.InlineKeyboardButton("Нет (пропустить этап)", callback_data='noSkip')
            markup.add(item1, item2)

            bot.send_message(call.message.chat.id, "У вас есть филиал?",
                             parse_mode='html', reply_markup=markup)

        # ВЕТКА ДОБАВЛЕНИЯ ФИЛИАЛА (callback_data = yesAdd)
        if call.data == 'yesAdd':
            global AddBravchList
            AddBravchList = []

            def AddBravch(AddBravchList):
                try:
                    print(AddBravchList)
                    number = AddBravchList[0]
                    address = AddBravchList[1]

                    # Подключение к существующей базе данных
                    connection = psycopg2.connect(user="postgres",
                                                  # пароль, который указали при установке PostgreSQL
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="BOT")

                    # Курсор для выполнения операций с базой данных
                    cursor = connection.cursor()
                    # Распечатать сведения о PostgreSQL
                    print("Информация о сервере PostgreSQL")
                    print(connection.get_dsn_parameters(), "\n")
                    # Выполнение SQL-запроса

                    cursor.execute(
                        f"INSERT INTO \"Branch\"  (\"number\", \"address\") VALUES('{number}', '{address}');")
                    connection.commit()

                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("Соединение с PostgreSQL закрыто")

            def finishBranch(message):

                AddBravchList.append(message.text)
                AddBravch(AddBravchList)
                add_rooms(call)

            def branchAdress(message):
                AddBravchList.append(message.text)

                msg = bot.send_message(call.message.chat.id, "Введите адрес филиала : ",
                                       parse_mode='html')
                bot.register_next_step_handler(msg, finishBranch)

            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, "Добавляем филиал. Введите его номер : ",
                                   parse_mode='html')
            bot.register_next_step_handler(msg, branchAdress)

        # ВЕТКА СКИП ФИЛИАЛА (callback_data = noSkip)
        if call.data == 'noSkip':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            add_rooms(call)

        # ДОБАВЛЕНИЕ ДОПОЛНИТЕЛЬНОГО КАБИНЕТА (callback_data = yesAddCab)
        if call.data == 'yesAddCab':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            add_rooms(call.message.chat.id)

        # ПЕРЕХОД К ДОБАВЛЕНИЮ СОТРУДНИКОВ (callback_data = noNext)
        if call.data == 'noNext':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            add_persons(call.message.chat.id)

        # ДОБАВЛЕНИЕ ПОДЧЕНЁННЫХ (callback_data = yesWork + noWork + yesSubWorkers + noSubWorkers)
        if call.data == 'yesWork' or call.data == 'noWork':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            haveSubWorkers(call.message.chat.id)

        if call.data == 'yesSubWorkers' or call.data == 'noSubWorkers':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            finishWorkers(call.message.chat.id)

        # КОНЕЦ РЕГИ,ВЫВОД БАЗЫ (callback_data = end)
        if call.data == 'end':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Здесь каким-то 🦀 будут выводиться данные базы...')
            time.sleep(4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1,
                                  text='Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!',
                                  reply_markup=main_menu(), parse_mode='html')

        # ДОБАВИТЬ ДОПОЛНИТЕЛЬНОГО СОТРУДНИКА (callback_data = yesAddPerson)
        if call.data == 'yesAddPerson':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            add_persons(call.message.chat.id)

        # ВХОД В СУЩЕСТВУЮЩУЮ БД (callback_data = login)
        if call.data == 'login':
            def loginCheck(message):
                if message.text == '12345':

                    bot.delete_message(call.message.chat.id, call.message.message_id - 1)
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Управление подченёнными", callback_data='subWorkersControle')
                    item2 = types.InlineKeyboardButton("Список корпоративных паролей", callback_data='passList')
                    item3 = types.InlineKeyboardButton("Список Клиентов", callback_data='clientsList')
                    item4 = types.InlineKeyboardButton("Добавить подчинённого", callback_data='addSubWorker')
                    item5 = types.InlineKeyboardButton("На главную", callback_data='back')
                    markup.add(item1, item2, item3, item4, item5)

                    bot.send_message(message.chat.id, "<b align='center'>МЕНЮ БАНКА</b>", parse_mode='html',
                                     reply_markup=markup)

                else:
                    bot.send_message(call.message.chat.id, f'Ваш проверочный код не верен.')
                    time.sleep(3)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 3,
                                          text='Добро пожаловать. Данный бот создан, что бы ты мог ничего не делать!',
                                          reply_markup=main_menu())

            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, f'Введите ваш персональный код : ')
            bot.register_next_step_handler(msg, loginCheck)

        # ДАННЫЕ ПО ПОДЧИНЁННЫМ КОНКРЕТНОГО ЛИЦА
        if call.data == 'subWorkersControle':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Здесь каким-то 🦀 будут выводиться данные базы...')
            time.sleep(4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1,
                                  text='<b align="center">МЕНЮ БАНКА</b>', reply_markup=db_menu(), parse_mode='html')

        # КОНТЕЙНЕР КОРП. ПАРОЛЕЙ
        if call.data == 'passList':
            def finishPassList(message):
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Добавить в базу", callback_data='addCorpPass')
                item2 = types.InlineKeyboardButton("Просмотреть имеющиеся данные", callback_data='watchGet')
                markup.add(item1, item2)

                bot.send_message(call.message.chat.id,
                                 "Выберите действие : (❗ВНИМАНИЕ не забудьте удалить введённые данные из чата ТГ, во избежание утечки информации.❗)",
                                 parse_mode='html', reply_markup=markup)

            def getData(message):
                msg = bot.send_message(call.message.chat.id, 'Введите GET данные : ', parse_mode='html')
                bot.register_next_step_handler(msg, finishPassList)

            def enterPass(message):
                msg = bot.send_message(call.message.chat.id, 'Введите пароль : ', parse_mode='html')
                bot.register_next_step_handler(msg, getData)

            def enterLogin(message):
                msg = bot.send_message(call.message.chat.id, 'Введите логин : ', parse_mode='html')
                bot.register_next_step_handler(msg, enterPass)

            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, '''Для доступа, войдите!
Введите ваш EMAIL: ''',
                                   parse_mode='html')
            bot.register_next_step_handler(msg, enterLogin)

        # ДОБАВЛЕНИЕ КОРП. ДАННЫХ В БД
        if call.data == 'addCorpPass':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Ваши данные типо были добавлены... (нет)')
            time.sleep(3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1,
                                  text='<b align="center">МЕНЮ БАНКА</b>', reply_markup=db_menu(), parse_mode='html')

        # ПРОСМОТР ИМЕЮЩИХСЯ ДАННЫХ
        if call.data == 'watchGet':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Тут могли быть ваши данные, но тут поселился 👽')
            time.sleep(4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1,
                                  text='<b align="center">МЕНЮ БАНКА</b>', reply_markup=db_menu(), parse_mode='html')

        # СПИСОК КЛИЕНТОВ
        if call.data == 'clientsList':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Здесь будут данные по клиентам, за которыми мы пристально 👁')
            time.sleep(4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1,
                                  text='<b align="center">МЕНЮ БАНКА</b>', reply_markup=db_menu(), parse_mode='html')

        # ДОБАВЛЕНИЕ ПОДЧИНЁННЫХ
        if call.data == 'addSubWorker':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            subAdd_person(call.message.chat.id)

        if call.data == 'subYesWork' or call.data == 'subNoWork':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            subHaveSubWorkers(call.message.chat.id)

        if call.data == 'sub1YesWork' or call.data == 'sub1NoWork':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            subFinish(call.message.chat.id)

        if call.data == 'subYesAddPerson':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            subAdd_person(call.message.chat.id)

        if call.data == 'subEnd':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='<b align="center">МЕНЮ БАНКА</b>', reply_markup=db_menu(), parse_mode='html')


# RUN
bot.polling(none_stop=True)
