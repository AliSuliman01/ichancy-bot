from models.gift import Gift

def validate( code , telegram_id):
    gift = Gift().getBy({'code' : ('=' , code) , 'telegram_goal_id' : ('=' , telegram_id)})
    if gift and not gift[0].get('redeemed_at'):
        print(gift[0].get('redeemed_at'))
        return gift[0]