import re


def extract(message):
    x = str(message).find('$')
    lower = x+1
    upper = x+3  # default upper of 3 chars
    try:
        if(str(message[x+3]) != ' '):
            if(str(message[x+3]).isalpha()):
                upper += 1
                if(str(message[x+4]).isalpha()):
                    upper += 1
                    if(str(message[x+5]).isalpha()):
                        upper += 1
                        if(str(message[x+6]).isalpha()):
                            upper += 1
    except IndexError:
        pass
    return message[lower:upper]
