import telebot
from telebot import types
import settings

client = telebot.TeleBot(settings.TOKEN)


@client.message_handler(commands=["start"])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rmk.add(types.KeyboardButton("Начать поиск"), types.KeyboardButton("Зарегистрироваться"))
    print("_user_answer")
    msg = client.send_message(message.chat.id, "Привет", reply_markup=rmk)
    client.register_next_step_handler(msg, user_answer)


def user_answer(message):
    print("_user_answer")
    if message.text == "Начать поиск":
        msg = client.send_message(message.chat.id, "Впишите станцию отправления")
        client.register_next_step_handler(msg, second_station)
        print(message.text)
    else:
        msg = client.send_message(message.chat.id, "Введите вашу почту")
        print(message.text)
        client.register_next_step_handler(msg, mail_reg)


def second_station(message):
    s_station = message.text
    print("_second_station")


def mail_reg(message):
    print("_mail_reg")
    mail = message.text


client.polling(none_stop=True, interval=0)
