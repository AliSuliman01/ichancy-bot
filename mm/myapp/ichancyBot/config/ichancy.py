from .settings import get_setting

# Bot configuration
PARENT_ID = get_setting('parent_id')

exchange_rate = get_setting('exchange_rate')
EXCHANGE_RATE = int(exchange_rate) if exchange_rate is not None else 1