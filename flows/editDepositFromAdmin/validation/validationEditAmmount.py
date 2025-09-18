


def validate(edit_ammount:str):
    if edit_ammount.isdigit():
        if int(edit_ammount) > 0:
            return True
    return False
