import api.index as api
from utils.get_mac_id import get_mac
import json
from scripts import Trial, Active, Expired
import os
from sys import exit

mac_address = get_mac()
response = api.get_user(mac_address)
os.system('color')
if(response == 'Not Found'):
    # register the user
    print('Enter you email id to register for trial plan')
    email_inp = input()
    res = api.register_trial_user(mac_address, email_inp)
    if(res == 'Success'):
        print(
            'Congrats you are now registered on the trial plan, Rerun the BOT to continue !')
    else:
        print('Couldn\'t register, please contact support')
        exit()
else:
    data = json.loads(response)
    if(data['status'] == 'Trial'):
        Trial.Trial(mac_add=mac_address)
    elif(data['status'] == 'Expired'):
        Expired.Expired()
    elif(data['status'] == 'Active'):
        Active.Active()
