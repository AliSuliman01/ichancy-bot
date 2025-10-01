
from models.user import User

def validation(user_id , cursor):
    if not User(cursor).getBy({'telegram_id' : ('=' , user_id)}):
        return True