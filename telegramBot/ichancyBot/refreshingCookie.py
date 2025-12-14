
from threading import Thread
import config.telegram
from datetime import datetime, timedelta
import time
from iChancyAPI import iChancyAPI
import Logger
from threadManager import get_thread_manager


class RefreshingCookieThread(Thread):
    """Thread for refreshing authentication cookies periodically."""
    
    def __init__(self):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        self.shutdown_event = get_thread_manager().shutdown_event
        
    def run(self):
        """Main thread loop for refreshing cookies."""
        self.logger.info("RefreshingCookie thread started")
        
        try:
            api = iChancyAPI()
            result = api.checkCookieIsWork()
            self.logger.info(f"Initial cookie check - Success: {result.get('success')}, Error: {result.get('error')}")     
            config.telegram.COOKIE_MESSAGE_SENT = False
        except Exception as e:
            self.logger.error(f"Error in initial cookie check: {e}", exc_info=True)
        
        while not self.shutdown_event.is_set():
            try:
                oldCookieTime = config.telegram.UPDATE_COOKIE_DATE
                cookieExpired = oldCookieTime + 1780.0
                current_timestamp = datetime.timestamp(datetime.now())
                
                if current_timestamp > cookieExpired:
                    self.logger.info(f"Cookie expired, refreshing... (expired: {cookieExpired}, current: {current_timestamp})")
                    api = iChancyAPI()
                    result = api.checkCookieIsWork()
                    self.logger.info(f"Cookie refresh result - Success: {result.get('success')}, Error: {result.get('error')}")    
                    config.telegram.COOKIE_MESSAGE_SENT = False
                    
                    # Wait with periodic checks for shutdown
                    if self.shutdown_event.wait(timeout=5.0):
                        break
                
                # Reset cookie message sent flag periodically
                timestamp_mod = int(current_timestamp) % 100
                if timestamp_mod in [0, 2, 3]:
                    config.telegram.COOKIE_MESSAGE_SENT = False
                    self.logger.debug(f"Reset COOKIE_MESSAGE_SENT flag (timestamp mod: {timestamp_mod})")
                
                # Wait with periodic checks for shutdown
                if self.shutdown_event.wait(timeout=3.0):
                    break
                    
            except Exception as e:
                self.logger.error(f"Error in RefreshingCookie thread: {e}", exc_info=True)
                if self.shutdown_event.wait(timeout=3.0):
                    break
        
        self.logger.info("RefreshingCookie thread stopped")