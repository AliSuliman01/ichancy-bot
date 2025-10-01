from models.model import Model

class User(Model):
    def __init__(self , cursor):
        super().__init__(cursor=cursor)
    def get_table(self):
        return "users"  
    
    