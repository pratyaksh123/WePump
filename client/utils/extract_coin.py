def extract(message):
    x = str(message).find("$")
    if x == -1:
        print("Failed to detect coin, enter manually")
        inp = input()
        return inp
    else:
        lower = x + 1
        upper = x + 3  # default upper of 3 chars
        try:
            if str(message[x + 3]) != " ":
                if str(message[x + 3]).isalpha():
                    upper += 1
                    if str(message[x + 4]).isalpha():
                        upper += 1
                        if str(message[x + 5]).isalpha():
                            upper += 1
                            if str(message[x + 6]).isalpha():
                                upper += 1
        except IndexError:
            pass
        return message[lower:upper]
