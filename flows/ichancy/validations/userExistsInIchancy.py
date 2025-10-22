

from models.user import User
from database import Database

def validation(user_id):
      db = Database.getConnection()
      try:
            if db:

                  cursor = db.cursor(dictionary=True)
                  if User(cursor).getBy({'telegram_id' : ('=' , user_id)})[0].get('player_id'):
                        db.close()
                        return True     
      except:
            ""

      finally:
            db.close()