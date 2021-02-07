import scripts.Common as common
import api.index as api
import json
import scripts.pump_take_profit as pump
import scripts.telegram as tel
import scripts.Check_balance as cb


def Active(mac_add):
    common.Common_Welcome("Premium")
    with open("./config.json") as f:
        data = json.load(f)
    first_menu = True
    while True:
        if not first_menu:
            common.Common_Menu()
        x = int(input())
        if x == 1:
            first_menu = False
            json_formatted_str = json.dumps(data, indent=2)
            print("Current Settings - ")
            print(json_formatted_str)
        elif x == 2:
            first_menu = False
            print("Do you wish to start the bot (Y/N) ?")
            inp = input()
            if inp == "Y" or inp == "y":
                pump.pump_take_profit(data, False)
        elif x == 3:
            # Test Telegram integration
            first_menu = False
            tel.Telegram(data, testMode=True)
        elif x == 4:
            first_menu = False
            print(cb.Check_balance(data))
        elif x == 5:
            exit()