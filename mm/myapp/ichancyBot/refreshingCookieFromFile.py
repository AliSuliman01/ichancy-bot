
from threading import Thread
import config.telegram
from datetime import datetime, timedelta
import time
import os
import Logger
from threadManager import get_thread_manager


class RefreshingCookieFromFileThread(Thread):
    """Thread for refreshing authentication cookies from a file."""
    
    def __init__(self, cookie_file_path: str = None):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        self.shutdown_event = get_thread_manager().shutdown_event
        
        # Use provided path or default to cross-platform path
        if cookie_file_path:
            self.cookie_file_path = cookie_file_path
        else:
            # Default to relative path from current working directory
            # Works on both Windows and Unix systems
            self.cookie_file_path = os.path.join("ichancyBot", "cookie.txt")
        
    def run(self):
        """Main thread loop for reading cookies from file."""
        # self.logger.info(f"RefreshingCookieFromFile thread started (watching: {self.cookie_file_path})")
        
        while not self.shutdown_event.is_set():
            try:
                if os.path.exists(self.cookie_file_path):
                    with open(self.cookie_file_path, 'r', encoding='utf-8') as f:
                        cookie = f.readline().replace("\n", "").strip()
                        if cookie and config.telegram.COOKIE_STRING != cookie:
                            config.telegram.COOKIE_STRING = cookie
                            config.telegram.COOKIE_STATUS = True
                            # self.logger.info("Cookie updated from file")
                        elif not cookie:
                            self.logger.warning("Cookie file is empty")
                else:
                    self.logger.debug(f"Cookie file not found: {self.cookie_file_path}")
                    
            except FileNotFoundError:
                self.logger.debug(f"Cookie file not found: {self.cookie_file_path}")
            except PermissionError:
                self.logger.error(f"Permission denied reading cookie file: {self.cookie_file_path}")
            except Exception as e:
                self.logger.error(f"Error reading cookie from file: {e}", exc_info=True)
            
            # Wait with periodic checks for shutdown
            if self.shutdown_event.wait(timeout=10.0):
                break
        
        # self.logger.info("RefreshingCookieFromFile thread stopped")
    



