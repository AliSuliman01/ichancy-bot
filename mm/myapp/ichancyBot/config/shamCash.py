from .settings import get_setting




SHAM_CASH_ACCOUNT = "739ceb70ab4a17ecc3317cb4ee46edc5"

MINIMUM_WITHDRAW = 25000

TAX = 0.1

shamcash_deposit_group_str = get_setting('shamcash_deposit_group')
SHAMCASH_DEPOSIT_GROUP = shamcash_deposit_group_str.split(" ")[0] if shamcash_deposit_group_str else None

shamcash_withdraw_group_str = get_setting('shamcash_withdraw_group')
SHAMCASH_WITHDRAW_GROUP = shamcash_withdraw_group_str.split(" ")[0] if shamcash_withdraw_group_str else None