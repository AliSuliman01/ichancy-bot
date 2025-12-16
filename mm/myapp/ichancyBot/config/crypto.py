from .settings import get_setting




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


crypto_deposit_group_str = get_setting("crypto_deposit_group")
CRYPTO_DEPOSIT_GROUP = crypto_deposit_group_str.split(" ")[0] if crypto_deposit_group_str else None

crypto_withdraw_group_str = get_setting("crypto_withdraw_group")
CRYPTO_WITHDRAW_GROUP = crypto_withdraw_group_str.split(" ")[0] if crypto_withdraw_group_str else None