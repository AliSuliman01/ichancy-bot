from config.bemo import MINIMUM_DEPOSITE


def validate(value):
    if  str.isdigit(value):
        if int(value) > MINIMUM_DEPOSITE:
            return True
    return False
