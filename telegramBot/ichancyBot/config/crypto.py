import os
from dotenv import load_dotenv

load_dotenv()




SYP_for_unit ={
    'SYP' : 1 , 
    'USDT' : None , 
    'USD' : None ,
}

WALLET_TYPE = r'USDT-TRC20|USDT-BEP20'
MINIMUM_DEPOSITE = 5
MINIMUM_WITHDRAW = 5
wallets = {
    "USDT-TRC20" : "examplezxcvbnmdfghjklexampleTRC20",
    "USDT-BEP20" : "examplezxcvbnmdfghjklexampleBEP20"
}


CRYPTO_DEPOSIT_GROUP =  os.getenv("CRYPTO_DEPOSIT_GROUP").split(" ")[0]
CRYPTO_WITHDRAW_GROUP= os.getenv("CRYPTO_WITHDRAW_GROUP").split(" ")[0]