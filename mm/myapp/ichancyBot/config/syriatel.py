from .settings import get_setting


SYRIATEL_ACCOUNT = "0997957092"

MINIMUM_DEPOSITE = 25000

MINIMUM_WITHDRAW = 100000

TAX = 0.1

syriatel_deposit_group_str = get_setting('syriatel_deposit_group')
SYRIATEL_DEPOSIT_GROUP = syriatel_deposit_group_str.split(" ")[0] if syriatel_deposit_group_str else None

syriatel_withdraw_group_str = get_setting('syriatel_withdraw_group')
SYRIATEL_WITHDRAW_GROUP = syriatel_withdraw_group_str.split(" ")[0] if syriatel_withdraw_group_str else None