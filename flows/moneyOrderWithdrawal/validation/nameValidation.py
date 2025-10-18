


def nameValidation(name:str):
    if len(name.split(" "))<3:
        return False
    for char in name:
        if char.isdigit():
            return False
    return True