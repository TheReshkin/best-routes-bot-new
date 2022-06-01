import telebot
import time
import reg.sign
import routes.avia
import settings
import sqlite3

from sub_data import iata
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


@bot.message_handler(commands=['date'])
def date_cal(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    date_r, key, step = DetailedTelegramCalendar().process(c.data)
    if not date_r and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif date_r:
        bot.edit_message_text(f"You selected {date_r}",
                              c.message.chat.id,
                              c.message.message_id)

        dep_code = iata.city_to_iata(str(db_table_get_f_station(c.message.from_user.id)))
        arrival_code = str(db_table_get_s_station(c.message.from_user.id))
        dep_date = str(date_r)
        answer = routes.avia.get_route(dep_code,
                                       arrival_code, dep_date, "Y")
        time.sleep(5)
        bot.send_message(c.message.chat.id, answer, parse_mode='Markdown') \
 \
        @bot.message_handler(commands=["start"])


def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if db_table_is_reg(message.from_user.id):
        rmk.add(types.KeyboardButton("Начать поиск"), types.KeyboardButton("Выйти из аккаунта"))
    else:
        rmk.add(types.KeyboardButton("Начать поиск"), types.KeyboardButton("Зарегистрироваться"))

    print("_user_answer")
    msg = bot.send_message(message.chat.id, "Привет, что нужно сделать?", reply_markup=rmk)
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
        bot.register_next_step_handler(msg, reg_mail)
    elif message.text == "Выйти из аккаунта":
        msg = bot.send_message(message.chat.id, "Выходим из аккаунта")
        bot.register_next_step_handler(msg, mail_out)


def second_station(message):
    # добавить проверку города
    f_station = message.text
    if iata.city_to_iata(f_station) is not None:
        print("_second_station")
        print(f_station)
        # добавляю в бд (будет проверка вводимых данных)
        db_table_f_station(message.from_user.id, f_station)
        msg = bot.send_message(message.chat.id, "Впишите станцию назначения")
        bot.register_next_step_handler(msg, route_date)
    else:
        msg = bot.send_message(message.chat.id, "Я не знаю такого города")
        bot.register_next_step_handler(msg, second_station)


def route_date(message):
    s_station = message.text
    print("_route_date")
    print(s_station)
    if iata.city_to_iata(s_station) is not None:
        # добавить проверку
        db_table_s_station(message.from_user.id, s_station)
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    else:
        msg = bot.send_message(message.chat.id, "Я не знаю такого города")
        bot.register_next_step_handler(msg, route_date)


def reg_mail(message):
    print("_reg_mail")
    mail = message.text
    # добавить проверку вводимых данных и целесообразности изменения личных данных
    db_table_user_id(message.from_user.id)
    db_table_mail(message.from_user.id, mail)
    msg = bot.send_message(message.chat.id, "Введите ваше кодовое слово (пароль)")
    bot.register_next_step_handler(msg, reg_password)


def reg_password(message):
    print("_reg_password")
    password = message.text
    db_table_password(message.from_user.id, password)
    msg = bot.send_message(message.chat.id, "Регистрация завершена, теперь у вас есть личный токен")
    db_table_token(message.from_user.id, reg.sign.register(db_table_get_mail(message.from_user.id),
                                                           db_table_get_password(message.from_user.id)))


def mail_out(message):
    print("_mail_out")
    # message.chat.id поиск по базе почты и пароля
    # добавить базу данных
    mail = db_table_get_mail(message.from_user.id)
    password = db_table_get_password(message.from_user.id)
    # sign.log_out(mail, password)
    # удаление данных из базы
    db_table_del_user(message.from_user.id)
    msg = bot.send_message(message.chat.id, "Вышли из аккаунта")


# запросы к базе данных работают только здесь, надо исправить
# первоначальное добавление в таблицу, не будет использоваться повторно
def db_table_val(user_id: int, mail: str, password: str, token: str):
    cursor.execute("INSERT INTO users (user_id, mail, password, token) VALUES (?, ?, ?, ?)",
                   (user_id, mail, password, token))
    conn.commit()


# первоначальное добавление в таблицу, не будет использоваться повторно
def db_table_user_id(user_id: int):
    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()


# добавление отдельно почты
def db_table_mail(user_id: int, mail: str):
    cursor.execute(f"UPDATE users SET mail=? WHERE user_id=?",
                   (mail, user_id))
    conn.commit()


# добавление отдельно пароля
def db_table_password(user_id: int, password: str):
    cursor.execute(f"UPDATE users SET password=? WHERE user_id=?",
                   (password, user_id))
    conn.commit()


def db_table_token(user_id: int, token: str):
    cursor.execute(f"UPDATE users SET token=? WHERE user_id=?",
                   (token, user_id))
    conn.commit()


# добавление города отправления в базу данных
def db_table_f_station(user_id: int, f_station: str):
    info = cursor.execute('SELECT * FROM user_stations WHERE user_id=?', (user_id,))

    if info.fetchone() is None:
        cursor.execute("INSERT INTO user_stations (user_id, f_station) VALUES (?, ?)",
                       (user_id, f_station))
        conn.commit()

    else:
        cursor.execute(f"UPDATE user_stations SET f_station=? WHERE user_id=?",
                       (f_station, user_id))
        conn.commit()


# добавление города назначения в базу данных
def db_table_s_station(user_id: int, s_station: str):
    # проверка на наличие в базе
    info = cursor.execute('SELECT * FROM user_stations WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        cursor.execute("INSERT INTO user_stations (user_id, f_station) VALUES (?, ?)",
                       (user_id, s_station))
        conn.commit()

    else:
        cursor.execute(f"UPDATE user_stations SET s_station=? WHERE user_id=?",
                       (s_station, user_id))
        conn.commit()


# удаление городов из базы данных
def db_table_del_station(user_id: int):
    cursor.execute("DELETE FROM user_stations (f_station, s_station) WHERE user_id (?)",
                   user_id)
    conn.commit()


# проверка на наличие регистрации
def db_table_is_reg(user_id: int):
    info = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        # Делаем когда нету человека в бд
        return False
    else:
        # Делаем когда есть человек в бд
        return True


def db_table_del_user(user_id: int):
    info = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        # Делаем когда нету человека в бд
        pass
    else:
        cursor.execute("DELETE FROM users WHERE user_id=(?)",
                       (user_id,))
        conn.commit()


def db_table_get_mail(user_id: int):
    mail = cursor.execute('SELECT mail FROM users WHERE user_id=?', (user_id,))
    print(mail)
    return mail


def db_table_get_password(user_id: int):
    password = cursor.execute('SELECT password FROM users WHERE user_id=?', (user_id,))
    print(password)
    return password


def db_table_get_token(user_id: int):
    token = cursor.execute('SELECT token FROM users WHERE user_id=?', (user_id,))
    print(token)
    return token


def db_table_get_f_station(user_id: int):
    f_station = cursor.execute("SELECT f_station FROM user_stations WHERE user_id=?", (user_id,))
    print(f_station)
    return f_station


def db_table_get_s_station(user_id: int):
    s_station = cursor.execute('SELECT s_station FROM user_stations WHERE user_id=?', (user_id,))
    print(s_station)
    return s_station


bot.polling(none_stop=True, interval=0)
