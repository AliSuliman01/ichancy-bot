from models.user import User


def ammountIsSuffecient(balance , giftAmmount):
    
    if giftAmmount >0 and giftAmmount <= balance:
        return True
