
from threading import Thread
import config.referal
from datetime import datetime, timedelta
import time
from models.user import User
from models.transaction import Transaction
import Logger
from database import Database
from threadManager import get_thread_manager


class referalThread(Thread):
    """Thread for processing referral rewards periodically."""
    
    def __init__(self):
        super().__init__(daemon=True)
        self.logger = Logger.getLogger()
        self.shutdown_event = get_thread_manager().shutdown_event

    def run(self):
        """Main thread loop for processing referral rewards."""
        # self.logger.info("Referral thread started")
        
        while not self.shutdown_event.is_set():
            try:
                self.logger.debug("Checking referral date for update")
                if config.referal.REFERAL_DATE < datetime.now(): 
                    config.referal.REFERAL_DATE = datetime.now()  
                    self.addBalanceForParent()  
                    config.referal.REFERAL_DATE = datetime.now() + timedelta(**config.referal.ROLL_TIME)
                    # self.logger.info(f"Updated referral date to: {config.referal.REFERAL_DATE}")
                
                # Wait with periodic checks for shutdown
                if self.shutdown_event.wait(timeout=60.0):
                    break
                    
            except Exception as e:
                self.logger.error(f"Error in referral thread: {e}", exc_info=True)
                if self.shutdown_event.wait(timeout=60.0):
                    break
        
        # self.logger.info("Referral thread stopped")

    def getParentReferalIDes(self, cursor):
        """Get mapping of parent referral IDs to their child user IDs."""
        # Use raw SQL for NULL check since Model.getBy doesn't handle IS NOT NULL properly
        cursor.execute("SELECT * FROM users WHERE referal_id IS NOT NULL")
        child_users = cursor.fetchall()
        parent_child_ides = {}
        for user in child_users:
            parent_id = user.get('referal_id')
            if parent_id is not None:
                if parent_id not in parent_child_ides:
                    parent_child_ides[parent_id] = []
                parent_child_ides[parent_id].append(user.get('id'))
        return parent_child_ides
    
    def addBalanceForParent(self):
        """Add referral balance to parent users based on their children's transactions."""
        db = Database.getConnection()
        try:
            if db:
                db.start_transaction()
                cursor = db.cursor(dictionary=True) 
                parent_child_ides = self.getParentReferalIDes(cursor)
                
                for parent_id in parent_child_ides.keys():
                    if len(parent_child_ides[parent_id]) < config.referal.MIN_NUM_OF_REFERALS:
                        self.logger.debug(f"Parent {parent_id} has insufficient referrals: {len(parent_child_ides[parent_id])} < {config.referal.MIN_NUM_OF_REFERALS}")
                        continue
                    
                    value = 0
                    for child_id in parent_child_ides[parent_id]:           
                        transactions = Transaction(cursor).getBy({
                            'user_id': ('=', child_id),
                            'created_at': ('>', config.referal.REFERAL_DATE - timedelta(**config.referal.ROLL_TIME)),
                            'status': ('=', 'approved')
                        })  
                        for transaction in transactions:
                            value += abs(transaction.get('value'))
                    
                    if value > 0:
                        parent_user = User(cursor).getById(parent_id)
                        if parent_user:
                            oldBalance = parent_user.get('balance')
                            newBalance = oldBalance + value * config.referal.REFERAL_PERCENT
                            User(cursor).update({'id': ('=', parent_id)}, {'balance': newBalance})
                            # self.logger.info(f"Updated balance for parent {parent_id}: {oldBalance} -> {newBalance} (added {value * config.referal.REFERAL_PERCENT})")
                
                db.commit()
        except Exception as e:
            self.logger.error(f"Error in addBalanceForParent: {e}", exc_info=True)
            if db:
                db.rollback()
        finally:
            if db:
                db.close()
          