import os
from dotenv import load_dotenv

load_dotenv()




SHAM_CASH_ACCOUNT = "739ceb70ab4a17ecc3317cb4ee46edc5"

MINIMUM_WITHDRAW = 25000

TAX = 0.1

SHAMCASH_DEPOSIT_GROUP  = os.getenv('SHAMCASH_DEPOSIT_GROUP').split(" ")[0]
SHAMCASH_WITHDRAW_GROUP = os.getenv('SHAMCASH_WITHDRAW_GROUP').split(" ")[0]