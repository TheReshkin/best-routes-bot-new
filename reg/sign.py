import json
import requests


def log_in(mail, password):
    url = "https://best-routes.herokuapp.com/user/login"
    mail = "resh@grail.com"
    password = "resh1"

    payload = json.dumps({
        "email": mail,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    if response.json().get('status') == 'OK':
        u_token = response.json().get('token')
        # добавление в базу данных
        return u_token
    else:
        # возвращает если пользователь не зарегистрирован
        return None


def log_out(mail, password):
    u_token = log_in(mail, password)
    url = "https://best-routes.herokuapp.com/user/quit"

    payload = {}
    headers = {
        'Token': u_token
    }
    if u_token is not None:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    # добавить удаление токена из базы данных


def register(mail, password):
    mail = "resh@grail.com"
    password = "resh1"
    url = "https://best-routes.herokuapp.com/user/register"

    payload = "{\n    \"email\":" + "\"" + mail + "\"" + ",\n    \"password\": " + "\"" + password + "\"" + "\n}"
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    print(payload)

    if response.json().get('status') == 'OK':
        u_token = response.json().get('token')
        return u_token
    else:
        return None
