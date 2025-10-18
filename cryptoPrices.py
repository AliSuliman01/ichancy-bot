import requests 
from datetime import datetime
import math
import config.crypto
import Logger
import time
from threading import Thread
class CryptoPrices(Thread):
    

    def __init__(self):
       super().__init__(daemon=True)
       self.logger = Logger.getLogger()


    def run(self):

        while True:
            try:

                response = requests.get(f"""https://sp-today.com/app_api/cur_damascus.json?{int(datetime.timestamp(datetime.now()))-1}""" )
                DAMUSD = None
                for row in response.json():
                    if row['name'] == "USD":
                       DAMUSD= row['bid']
                       config.crypto.SYP_for_unit['USD'] = DAMUSD
                       break
                response = requests.get(f"""https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT""")
                DAMUSDT = math.ceil((float(response.json()['price'])*float(DAMUSD) + 100.0 +100.0))
                while DAMUSDT %100 !=0:
                    DAMUSDT-=1
                config.crypto.SYP_for_unit['USDT'] = DAMUSDT
                print(config.crypto.SYP_for_unit['USDT'])
                time.sleep(10)
            except Exception as e:
                self.logger.info(f"Error in request cryptoPrices {e}")
                time.sleep(1)
                return self.run()
           