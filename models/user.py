from models.model import Model

class User(Model):
    
    def get_table(self):
        return "users"  
    
    