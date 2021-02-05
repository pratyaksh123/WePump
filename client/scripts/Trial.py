import scripts.Common as common
import api.index as api
import json
import scripts.pump_take_profit as pump


def set_status_to_expire(mac_add):
    res = api.update_user_status(mac_add, 'Expired')
    if(res != 'Success'):
        print('Fatal Error, Please contact support')


def Trial(mac_add):
    common.Common_Welcome('Trial')
    with open('./config.json') as f:
        data = json.load(f)
    first_menu = True
    while True:
        if(not first_menu):
            common.Common_Menu()
        x = int(input())
        if(x == 1):
            first_menu = False
            json_formatted_str = json.dumps(data, indent=2)
            print("Current Settings - ")
            print(json_formatted_str)
        elif(x == 2):
            first_menu = False
            print('Do you wish to start the bot (Y/N) ?')
            inp = input()
            if(inp == 'Y' or inp == 'y'):
                pump.pump_take_profit(data)
                set_status_to_expire(mac_add)
                exit()
        elif(x == 3):
            exit()
