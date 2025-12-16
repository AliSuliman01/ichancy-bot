from models.model import Model

class AccountTransaction(Model):
    

    def get_table(self):
        return "account_transactions"