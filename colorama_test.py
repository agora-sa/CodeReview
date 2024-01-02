is_find = False

def abc():
    if is_find:
        print('123')

def bcd():
    global is_find
    is_find = True