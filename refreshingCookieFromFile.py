
from threading import Thread
import config.telegram
from datetime import datetime , timedelta
import time
from iChancyAPI import iChancyAPI
import Logger
import config.telegram
class RefreshingCookieFromFileThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        
    def run(self):
        while True:
            try:
                with open ("cookie.txt" , 'r') as f:
                    cookie = f.readline().replace("\n","").strip()
                    if config.telegram.COOKIE_STRING != cookie:
                        config.telegram.COOKIE_STRING = cookie
            except:
                self.logger.info("there is an error in refreshing cookie from file")
                print("there is an error in refreshing cookie from file")
            time.sleep(10)
    



