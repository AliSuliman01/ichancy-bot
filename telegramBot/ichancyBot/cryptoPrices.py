import requests 
from datetime import datetime
import math
import config.crypto
import Logger
import time
from threading import Thread
from threadManager import get_thread_manager


class CryptoPrices(Thread):
    """Thread for periodically fetching and updating cryptocurrency prices."""

    def __init__(self):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        self.shutdown_event = get_thread_manager().shutdown_event

    def run(self):
        """Main thread loop for fetching crypto prices."""
        self.logger.info("CryptoPrices thread started")
        
        while not self.shutdown_event.is_set():
            try:
                # Fetch USD rate
                response = requests.get(
                    f"https://sp-today.com/app_api/cur_damascus.json?{int(datetime.timestamp(datetime.now()))-1}",
                    timeout=10
                )
                response.raise_for_status()
                
                DAMUSD = None
                for row in response.json():
                    if row['name'] == "USD":
                        DAMUSD = row['bid']
                        config.crypto.SYP_for_unit['USD'] = DAMUSD
                        break
                
                if DAMUSD is None:
                    self.logger.warning("USD rate not found in response")
                    time.sleep(10)
                    continue
                
                # Fetch USDT rate
                response = requests.get(
                    "https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT",
                    timeout=10
                )
                response.raise_for_status()
                
                DAMUSDT = math.ceil((float(response.json()['price']) * float(DAMUSD) + 100.0 + 100.0))
                while DAMUSDT % 100 != 0:
                    DAMUSDT -= 1
                config.crypto.SYP_for_unit['USDT'] = DAMUSDT
                self.logger.debug(f"Updated USDT rate: {config.crypto.SYP_for_unit['USDT']}")
                
                # Wait with periodic checks for shutdown
                for _ in range(10):
                    if self.shutdown_event.wait(timeout=1.0):
                        break
                        
            except requests.RequestException as e:
                self.logger.warning(f"Network error in cryptoPrices: {e}")
                if self.shutdown_event.wait(timeout=5.0):
                    break
            except Exception as e:
                self.logger.error(f"Unexpected error in cryptoPrices: {e}", exc_info=True)
                if self.shutdown_event.wait(timeout=5.0):
                    break
        
        self.logger.info("CryptoPrices thread stopped")
           