from config.syriatel import MINIMUM_WITHDRAW 


def vlueValidate(value):
    if  str.isdigit(value):
        if int(value) > MINIMUM_WITHDRAW:
                return True
    return False



def balanceValidate(value , balance):
    if int(value) <= balance:
          return True
    return False
