import scripts.Common as common
import api.index as api


def Trial(mac_add):
    common.Common('Trial')
    # x = int(input())
    res = api.upadate_user_status(mac_add, 'Expired')
    if(res != 'Success'):
        print('Fatal Error, Please contact support')
