import telebot
import settings
import sqlite3

from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from reg import sign
from database import subd

bot = telebot.TeleBot(settings.TOKEN)

try:
    # база данных для хранения данных клиентов
    conn = sqlite3.connect('database/user_database.db', check_same_thread=False)
    cursor = conn.cursor()
except sqlite3.Error as error:
    print("Error:", error)


@bot.message_handler(commands=["start"])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    us_reg = False
    # добавить проверку на наличие регистрации
    if us_reg:
        rmk.add(types.KeyboardButton("Начать поиск"), types.KeyboardButton("Выйти из аккаунта"))
    else:
        rmk.add(types.KeyboardButton("Начать поиск"), types.KeyboardButton("Зарегистрироваться"))
    print("_user_answer")
    msg = bot.send_message(message.chat.id, "Привет", reply_markup=rmk)
    print(message.chat.id)
    bot.register_next_step_handler(msg, user_answer)


def user_answer(message):
    print("_user_answer")
    if message.text == "Начать поиск":
        msg = bot.send_message(message.chat.id, "Впишите станцию отправления")
        bot.register_next_step_handler(msg, second_station)
        print(message.text)
    elif message.text == "Зарегистрироваться":
        msg = bot.send_message(message.chat.id, "Введите вашу почту для регистрации")
        print(message.text)
        # добавление в базу данных информации о юзере, почему-то не работает
        cursor.execute("INSERT INTO users (user_id, mail, password, token) VALUES (?, ?, ?, ?)",
                       (message.chat.id, "resh@gmail.com", "pass123", "23457yfc"))
        conn.commit()

        bot.register_next_step_handler(msg, reg_mail)
    else:
        msg = bot.send_message(message.chat.id, "Выходим из аккаунта")
        print(message.text)
        bot.register_next_step_handler(msg, mail_out)


def second_station(message):
    s_station = message.text
    print("_second_station")


def reg_mail(message):
    print("_reg_mail")
    mail = message.text
    msg = bot.send_message(message.chat.id, "Введите ваше кодовое слово (пароль)")
    bot.register_next_step_handler(msg, reg_password)


def reg_password(message):
    print("_reg_password")
    password = message.text


def mail_out(message):
    print("_mail_out")
    # message.chat.id поиск по базе почты и пароля
    # добавить базу данных
    mail = "resh@gmail.com"
    password = "pass123"
    sign.log_out(mail, password)
    bot.send_message(message.chat.id, "Вышли из аккаунта")


@bot.message_handler(commands=['date'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


# запросы к базе данных работают только здесь, надо исправить
def db_table_val(user_id: int, mail: str, password: str, token: str):
    cursor.execute("INSERT INTO users (user_id, mail, password, token) VALUES (?, ?, ?, ?)",
                   (user_id, mail, password, token))
    conn.commit()


def db_table_chat_id(user_id: int):
    cursor.execute("INSERT INTO users (user_id) VALUES (?)",
                   (user_id))
    conn.commit()


# добавление города отправления в базу данных
def db_table_f_station(user_id: int, f_station: str):
    cursor.execute("INSERT INTO user_stations (user_id, f_station) VALUES (?, ?)",
                   (user_id, f_station))
    conn.commit()


# добавление города назначения в базу данных
def db_table_s_station(user_id: int, s_station: str):
    cursor.execute("INSERT INTO user_stations (user_id) VALUES (?, ?)",
                   (user_id, s_station))
    conn.commit()


# добавление города назначения в базу данных
def db_table_del_station(user_id: int):
    cursor.execute("INSERT INTO user_stations (user_id) VALUES (?)",
                   (user_id))
    conn.commit()


bot.polling(none_stop=True, interval=0)
