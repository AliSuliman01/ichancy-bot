from .settings import get_setting



BEMO_ACCOUNT = "1234567890BEMO"


MINIMUM_DEPOSITE = 25000

MINIMUM_WITHDRAW = 100000

TAX = 0.1



bemo_deposit_group_str = get_setting("bemo_deposit_group")
BEMO_DEPOSIT_GROUP = bemo_deposit_group_str.split(" ")[0] if bemo_deposit_group_str else None

bemo_withdraw_group_str = get_setting("bemo_withdraw_group")
BEMO_WITHDRAW_GROUP = bemo_withdraw_group_str.split(" ")[0] if bemo_withdraw_group_str else None