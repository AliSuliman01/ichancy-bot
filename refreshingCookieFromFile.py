
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
                    
                    print(cookie)
                    print("###################################")
                    print(config.telegram.COOKIE_STRING)
            except:
                self.logger.info("there is an error in refreshing cookie from file")
                print("there is an error in refreshing cookie from file")
            time.sleep(10)
        api = iChancyAPI()
        result = api.checkCookieIsWork()
        self.logger.info(f"API FOR REFRESH COOKIE WITH RESULT {result.get('success')}" + "    " + f"{result.get('error')}")     
        config.telegram.COOKIE_MESSAGE_SENT = False
        while True:
            oldCookieTime = config.telegram.UPDATE_COOKIE_DATE
            cookieExpired = oldCookieTime + 1780.0
            if datetime.timestamp(datetime.now()) > cookieExpired :
                api = iChancyAPI()
                result = api.checkCookieIsWork()
                self.logger.info(f"API FOR REFRESH COOKIE WITH RESULT {result.get('success')}" + "    " + f"{result.get('error')}")    
                config.telegram.COOKIE_MESSAGE_SENT = False
                print(cookieExpired)
                print(oldCookieTime)
                time.sleep(5)
            
            if int(datetime.timestamp(datetime.now()))%100 == 0 or int(datetime.timestamp(datetime.now()))%100 == 3 or int(datetime.timestamp(datetime.now()))%100 == 2:
                        config.telegram.COOKIE_MESSAGE_SENT = False
                        print(config.telegram.COOKIE_MESSAGE_SENT)
            time.sleep(3)



