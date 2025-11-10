from config.crypto import MINIMUM_DEPOSITE


def validate(value:str):
   
    if  str.isdigit(value):
        if int(value) >= MINIMUM_DEPOSITE:
            return True
    return False
