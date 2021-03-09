from termcolor import colored
import api.index as api

def change_password(mac_id):
    print('Fetching your current password')
    response= api.get_password_mac_id(mac_id)
    if(response!='false'):
        print(response)
        print(colored('Enter your new password','yellow'))
        password=input()
        res_1= api.update_password(mac_id,password)
        if(res_1=='Success'):
            print(colored('Your Password has been changed','green'))
        else:
            print('Failed to change your password , contact admin')
    else:
        print('Failed to get your password , contact admin')
    