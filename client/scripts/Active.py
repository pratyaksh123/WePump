import scripts.Common as common
import api.index as api
import json
import scripts.index as pump
import scripts.change_password as pass_fuck
import scripts.telegram as tel
import scripts.print_channel_ids as chn
import scripts.Check_balance as cb
from termcolor import colored
from sys import exit


def Active(mac_id):
    try:
        with open("./config.json") as f:
            data = json.load(f)
        common.Common_Welcome("Premium")
        first_menu = True
        while True:
            if not first_menu:
                common.Common_Menu()
            x = input()
            if x == "1":
                first_menu = False
                json_formatted_str = json.dumps(data, indent=2)
                print("Current Settings - ")
                print(json_formatted_str)
            elif x == "2":
                first_menu = False
                print("Do you wish to start the bot (Y/N) ?")
                inp = input()
                if inp == "Y" or inp == "y":
                    pump.main(data, False)
            elif x == "3":
                # Test Telegram integration
                first_menu = False
                tel.Telegram(data)
            elif x == "4":
                first_menu = False
                print(cb.Check_balance(data))
            elif x == "5":
                first_menu = False
                chn.channel_id(data)
            elif x=='6':
                first_menu = False
                pass_fuck.change_password(mac_id)
            elif x == "7":
                exit()
            else:
                first_menu = False
                print(colored("Wrong Input Given", "yellow"))
    except ValueError as e:
        print(e)
        print(colored("Please Recheck your config.json", "red"))
