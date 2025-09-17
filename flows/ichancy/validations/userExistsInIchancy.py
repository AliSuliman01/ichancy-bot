

from models.user import User

def validation(user_id):
      if User().getBy({'telegram_id' : ('=' , user_id)})[0].get('player_id'):
            return True          