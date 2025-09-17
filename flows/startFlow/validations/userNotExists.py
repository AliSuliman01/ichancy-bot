
from models.user import User
def validation(user_id):
    if not User().getBy({'telegram_id' : ('=' , user_id)}):
        return True