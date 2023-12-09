import requests
from settings import API_URL, AUTH_PORT, users, last_alert_id
from user import User
from json import loads

def login(id, login, password) -> bool:
    url = API_URL + ":" + AUTH_PORT + "/auth/token"
    data = {
        "username": login,
        "password": password
    }

    headers = {
        "accept": "application/json"
    }

    response = requests.post(url, data=data, headers=headers)

    return response

def get_alert():
    url = 'http://26.65.125.199:8004/alerts/last'

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return loads(response.text)


def get_profile(token):
    url = 'http://26.65.125.199:8004/users/me'

    headers = {
        "Authorization": "Bearer " + token,
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return loads(response.text)

def get_history(token):
    url = 'http://26.65.125.199:8004/tests/getHistoryUser'

    headers = {
        "Authorization": "Bearer " + token,
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return loads(response.text)

def get_rating():
    url = 'http://26.65.125.199:8004/users/getRating'

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return loads(response.text)