
from threading import Thread
import config.telegram
from datetime import datetime , timedelta
import time
from iChancyAPI import iChancyAPI
import Logger
class RefreshingCookieThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        
    def run(self):
        # time.sleep(5)
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