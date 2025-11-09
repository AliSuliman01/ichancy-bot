from config.crypto import MINIMUM_WITHDRAW
import config.crypto

def validate(value):
    if  str.isdigit(value):
        if int(value) >= MINIMUM_WITHDRAW:
            return True
    return False

def balanceValidate(value , balance , currency_name):
    if float(value)*float(config.crypto.SYP_for_unit[currency_name]) <= balance:
          return True
    return False