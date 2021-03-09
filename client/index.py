import api.index as api
from utils.get_mac_id import get_mac
import json
from scripts import Trial, Active, Expired
from termcolor import colored
import os
from sys import exit

mac_address = get_mac()
response = api.get_user(mac_address)
os.system("color")
if response == "false":
    print("Please enter your email address to sign-in/register.")
    email_inp = input()
    print("Enter password")
    password = input()
    # First check if this email already exists.
    res_sign_in= api.check_email(email_inp)
    if(res_sign_in=='true'):
        # Email found already registered, to check auth , check the password too.
        print(colored('Email Already Registered with the BOT, signing in...','yellow'))
        res_pass= api.get_password(password)
        if(res_pass=='true'):
            # True Account owner, but his mac address got changed, so update his previous account with the new mac id.
            res_update_mac_id= api.update_mac_id(email_inp,mac_address)
            if(res_update_mac_id=='true'):
                print(
                colored(
                    "Welcome back, you are now signed in ! Please Rerun the bot to continue.",
                    "green",))
                exit()
            elif(res_update_mac_id=='false'):
                print(colored("Couldn't Login, please contact support, error code - 0X112", "yellow"))
                exit()
            else:
                print(colored("Couldn't Login, please contact support, error code - 0X113", "yellow"))
                exit()
        elif(res_pass=='false'):
            print(colored('Email and Password didn\'t matched','red'))
        else:
            print(colored("Couldn't Login, please contact support, error code - 0X114", "yellow"))
            exit()
    elif(res_sign_in=='false'):
        # New Account
        res = api.register_trial_user(mac_address, email_inp,password)
        if res == "Success":
            print(
                colored(
                    "Congrats you are now registered on the trial plan, Rerun the BOT to continue !",
                    "green",
                )
            )
        else:
            print(colored("Couldn't register, please contact support, error code 0X115", "yellow"))
            exit()
    else:
        print(colored("Couldn't register, please contact support, error code 0X116", "yellow"))
        exit()
else:
    data = json.loads(response)
    if data["status"] == "Trial":
        timeleft=api.time_trial_left(data['mac_id'])
        print(colored(f'Your Trial Plan will expire on - {timeleft}','yellow'))
        Trial.Trial(mac_address)
    elif data["status"] == "Expired":
        Expired.Expired()
    elif data["status"] == "Active":
        Active.Active(mac_address)
