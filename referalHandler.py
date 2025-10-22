
from threading import Thread
import config.referal
from datetime import datetime , timedelta
import time
from models.user import User
from models.transaction import Transaction
import Logger
from database import Database
class referalThread(Thread):
    def __init__(self):
        super().__init__(daemon = True)
        self.logger = Logger.getLogger()


    def run(self):
       
        while True:
            self.logger.info("TRY UPDATE REFERAL DATE")
            if config.referal.REFERAL_DATE < datetime.now(): 
                config.referal.REFERAL_DATE = datetime.now()  
                self.addBalanceForParent()  
                config.referal.REFERAL_DATE = datetime.now() + timedelta(**config.referal.ROLL_TIME)
                
            time.sleep(60)
                

    def getParentReferalIDes(self , cursor):
        child_users =  User(cursor).getBy({'referal_id' : ('!=' , "NULL")})
        parent_child_ides = {}
        for user in child_users:
            parent_child_ides[user.get('referal_id')] = []
        for user in child_users:
            parent_child_ides[user.get('referal_id')].append(user.get('id'))
        return parent_child_ides
    
    def addBalanceForParent(self):
      db = Database.getConnection()
      try:
        if db:
            db.start_transaction()
            cursor = db.cursor(dictionary=True) 
            parent_child_ides = self.getParentReferalIDes(cursor)
            for parent_id in parent_child_ides.keys():
                if len(parent_child_ides[parent_id])< config.referal.MIN_NUM_OF_REFERALS:            
                    return False
                value = 0
                for child_id in parent_child_ides[parent_id]:           
                    transactions = Transaction(cursor).getBy({'user_id':('=' , child_id) ,'created_at' : (">" , config.referal.REFERAL_DATE - timedelta(**config.referal.ROLL_TIME))
                                                                        , 'status':('=' , 'approved')})  
                    for transaction in transactions:
                        value+= abs(transaction.get('value'))
                parent_user = User(cursor).getById(parent_id)
                oldBalance = parent_user.get('balance')
                newBalance = oldBalance + value*config.referal.REFERAL_PERCENT
                User(cursor).update({'id' :('=',parent_id)},{'balance' : newBalance})
                db.commit()
      except Exception as e:
          print (e)
          db.rollback()
      finally:
          db.close()
          