import os
from dotenv import load_dotenv

load_dotenv()



BEMO_ACCOUNT = "1234567890BEMO"


MINIMUM_DEPOSITE = 25000

MINIMUM_WITHDRAW = 100000

TAX = 0.1



BEMO_DEPOSIT_GROUP =  os.getenv("BEMO_DEPOSIT_GROUP").split(" ")[0]
BEMO_WITHDRAW_GROUP= os.getenv("BEMO_WITHDRAW_GROUP").split(" ")[0]