import scripts.Common as common
import api.index as api
import json
import scripts.index as pump
import scripts.telegram as tel
import scripts.print_channel_ids as chn
import scripts.Check_balance as cb
from termcolor import colored
from sys import exit


def set_status_to_expire(mac_add):
    res = api.update_user_status(mac_add, "Expired")
    if res != "Success":
        print("Fatal Error, Please contact support")


def Trial(mac_add):
    try:
        with open("./config.json") as f:
            data = json.load(f)
        common.Common_Welcome("Trial")
        first_menu = True
        while True:
            if not first_menu:
                common.Common_Menu()
            x = input()
            if x == '1':
                first_menu = False
                json_formatted_str = json.dumps(data, indent=2)
                print("Current Settings - ")
                print(json_formatted_str)
            elif x == '2':
                first_menu = False
                print("Do you wish to start the bot (Y/N) ?")
                inp = input()
                if inp == "Y" or inp == "y":
                    pump.main(data, True)
            elif x == '3':
                # Test Telegram integration
                first_menu = False
                tel.Telegram(data)
            elif x == '4':
                first_menu = False
                print(cb.Check_balance(data))
            elif x == '5':
                first_menu = False
                chn.channel_id(data)
            elif x == '6':
                exit()
            else:
                first_menu = False
                print(colored('Wrong Input Given', 'yellow'))
    except ValueError as e:
        print(e)
        print(colored('Please Recheck your config.json', 'red'))
