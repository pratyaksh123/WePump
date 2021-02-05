import requests

BASE_URL = 'https://us-central1-pump-bot-e1abf.cloudfunctions.net/app/api'


def get_user(mac_add):
    res = requests.get(BASE_URL+'/read/'+mac_add)
    if(res.status_code == 200):
        return res.text
    else:
        return res.reason


def register_trial_user(mac_add, email):
    data = {"mac_id": mac_add, "email_id": email}
    res = requests.post(BASE_URL+'/register-trial', data=data)
    if(res.status_code == 200):
        return res.text
    else:
        return res.reason


def upadate_user_status(mac_add, status):
    data = {"status": status}
    res = requests.put(BASE_URL+'/update/'+mac_add, data=data)
    if(res.status_code == 200):
        return res.text
    else:
        return res.reason
