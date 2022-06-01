import json

import requests


# установить библиотеку для поиска аэропортов по ИАТО
# import airportsdata

def avia_search(f_station, s_station, date):
    print("Avia")
    return edit_answer()


def avia_search(inline_query, num=5):
    print("Avia")
    return edit_answer_query(num)


def edit_answer_query(num):
    f_station = "Москва"
    s_station = "Санкт-Петербург"
    t_num = "1"
    # departure
    dep_date = "01.01.2022"
    dep_time = "09:00"
    # arrival
    arr_date = "01.01.2022"
    arr_time = "14:00"
    travel_time = "7:00"
    company = "Победа"
    link = "aviasales.ru"
    num_seats = "10"
    min_price = "2400"

    if num > 0:
        answer = f"""🛫 {num}
        {f_station}➡️{s_station}
        🕐 Отправление: {dep_time}  {dep_date}
        🕗 Прибытие: {arr_time}  {arr_date}
        ⏰ Время в пути: {travel_time}
        {num_seats} мест от {min_price} ₽
        Перевозчик: {company}
        Ссылка: {link}""" + \
                 "\n" + \
                 edit_answer_query(num - 1) if num > 0 else """ """
    else:
        return ""
    return answer


def edit_answer(s_station, f_station, dep_time, dep_date, arr_time, arr_date, travel_time, min_price, link,
                num_seats="не доступно", company="не отображено"):
    if company == "не отображено" and num_seats == "не доступно":
        answer = f"""🛫 {1}
        {f_station}➡{s_station}
        🕐 Отправление:{dep_date}
        🕗 Прибытие:{arr_date}
        ⏰ Время в пути: {travel_time} минут
        Места от {min_price} ₽
        Ссылка:{link}"""
    else:
        # выбрать где парсить дату
        answer = f"""🛫 {1}
        {f_station}➡{s_station}
        🕐 Отправление:{dep_date}
        🕗 Прибытие:{arr_date}
        ⏰ Время в пути:{travel_time}
        {num_seats}мест от{min_price} ₽
        Перевозчик:{company}
        Ссылка:{link}"""
    return answer


def get_route(dep_code, arrival_code, dep_date, service_class, adult=1, child=0, infant=0, count=-1):
    # отправления/прибытия указывать из городов
    # исправить добавление параметров
    url = "https://best-routes.herokuapp.com//routes/avia?departureCode=" + dep_code + "&arrivalCode=" + arrival_code + "&departureDate=" \
          + str(dep_date) + "&adult=" + str(adult) + "&child=" + str(child) + "&infant=" + \
          str(infant) + "&serviceClass=" + service_class + "&count=" + str(count)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = response.json()
    print(res_json)
    # добавить проверку корректности ответа
    # добавить вывод пересадок и поправить отображение билета
    route = res_json.get('result')[0]
    if count == 1:
        return edit_answer(route.get('arrival'), route.get('departure'), route.get('arrivalDateTime'),
                           route.get('arrivalDateTime'), route.get('departureDateTime'), route.get('departureDateTime'),
                           route.get('duration'),
                           route.get('places')[0].get('minPrice'), route.get('url'))
    else:
        answer = ""
        for i in range(count):
            answer += "pass"
            return answer
