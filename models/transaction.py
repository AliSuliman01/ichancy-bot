from models.model import Model

class Transaction(Model):
    
    def __init__(self , cursor):
        super().__init__(cursor=cursor)
    def get_table(self):
        return "transactions"