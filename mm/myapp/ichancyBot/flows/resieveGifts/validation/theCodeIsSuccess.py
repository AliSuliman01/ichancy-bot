from models.gift import Gift
from database import Database
def validate( code , telegram_id):
    db = Database.getConnection()
    try:
        if db:
            cursor = db.cursor(dictionary = True)
            gift = Gift(cursor).getBy({'code' : ('=' , code) , 'telegram_goal_id' : ('=' , telegram_id)})
            if gift and not gift[0].get('redeemed_at'):
                # print(gift[0].get('redeemed_at'))
                db.close()
                return gift[0]

    except :
        ""
    finally:
        db.close()