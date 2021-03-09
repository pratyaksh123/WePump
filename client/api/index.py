import requests
from termcolor import colored

# BASE_URL = "https://us-central1-pump-bot-e1abf.cloudfunctions.net/app/api"
BASE_URL = 'http://localhost:5001/pump-bot-e1abf/us-central1/app/api'


def get_user(mac_add):
    res = requests.get(BASE_URL + "/read/" + mac_add)
    if res.status_code == 200:
        return res.text
    else:
        print(colored('Something Went wrong contact admin','rec'))
        exit()


def register_trial_user(mac_add, email, password):
    data = {"mac_id": mac_add, "email_id": email, "password": password}
    res = requests.post(BASE_URL + "/register-trial", data=data)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason


def check_user(email_id,password):
    res = requests.get(BASE_URL + "/check_user/" + email_id+"/" + password)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason


def update_mac_id(email_id, mac_id):
    data = {"mac_id": mac_id}
    res = requests.put(BASE_URL + "/update_mac_id/" + email_id, data=data)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason

def get_password_mac_id(mac_id):
    res = requests.get(BASE_URL + "/get_password_mac_id/" + mac_id)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason

def update_password(mac_id, password):
    data = {"password": password}
    res = requests.put(BASE_URL + "/update_password/" + mac_id, data=data)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason
    
def time_trial_left(mac_id):
    res = requests.get(BASE_URL + "/get_time_left/" + mac_id)
    if res.status_code == 200:
        return res.text
    else:
        return res.reason