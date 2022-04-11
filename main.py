from telebot import types
from cards_1 import parser
from pacre import parser_1
import telebot
import sqlite3
bot = telebot.TeleBot("5176929450:AAEh-bNHd8prEP1UZe2ER-js6eW9hv3qrwA")



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! введите /choice ')
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()


    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    id INTEGER
    user_name VARCHAR
    )""")

    connect.commit()
    #отмена повторного добавления
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    #Переменная с данными пользователя
    data = cursor.fetchone()
    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id id VALUES(?);", user_id)
        connect.commit()


@bot.message_handler(commands=['delete'])
def delete(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()


    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()


@bot.message_handler(commands=['choice'])
def get_text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('💳 Кредитные')
    item2 = types.KeyboardButton('💳 Дебетовые')
    markup.add(item1, item2)
    mess = f'<b>  Привет, я чат бот для парсинга карт на сайте https://minfin.com.ua/cards/credit/ \n Какие карты тебе надо спарсить?  </b>'
    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == "private":
        if message.text == '💳 Кредитные':
            parser()
            doc = open(r'C:\Users\мвидео\PycharmProjects\pythonProject1\cards.csv', 'rb')
            bot.send_document(message.from_user.id, doc)
            doc.close()
        elif message.text == '💳 Дебетовые':
            parser_1()
            doc = open(r'C:\Users\мвидео\PycharmProjects\pythonProject1\cards1.csv', 'rb')
            bot.send_document(message.from_user.id, doc)
            doc.close()






#@bot.message_handler()
#def get_user_text(message):
    #if message.text == 'Hello':
        #bot.send_message(message.chat.id, "И ТЕБЕ БРАТАНр НЕ ХВАРАТЬ !!!", parse_mode='html')
    #elif message.text == 'id':
        #bot.send_message(message.chat.id, f"Твой ID:{message.from_user.id}")
    #elif message.text == 'photo':
        #photo = open('russian-hacker-linkedin-twaggies.jpg', 'rb')
        #bot.send_photo(message.chat.id, photo)
    #else:
        #bot.send_message(message.chat.id, "я тебя не понимаю ", parse_mode='html')



bot.polling()