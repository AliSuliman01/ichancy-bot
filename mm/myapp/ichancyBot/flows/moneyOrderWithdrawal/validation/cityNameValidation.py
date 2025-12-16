
from config.orderMoney import CITIES
def cityNameValidation(cityName:str):
    for char in cityName:
        if char.isdigit():
            return False
        if cityName not in CITIES:
            return False
    return True
