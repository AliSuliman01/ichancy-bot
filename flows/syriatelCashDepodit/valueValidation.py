from config.telegram import TRANSFEER_AMMOUNT


def validate(value):
    if  str.isdigit(value):
        if int(value) > TRANSFEER_AMMOUNT:
            return True
    return False
