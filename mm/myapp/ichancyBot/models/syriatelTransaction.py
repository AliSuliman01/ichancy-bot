from models.model import Model

class SyriatelTransaction(Model):
    def __init__(self , cursor):
        super().__init__(cursor=cursor) 

    def get_table(self):
        return "syriatel_transactions"