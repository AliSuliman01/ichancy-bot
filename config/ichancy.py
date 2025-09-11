import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
PARENT_ID = os.getenv('PARENT_ID')

EXCHANGE_RATE = os.getenv('EXCHANGE_RATE')