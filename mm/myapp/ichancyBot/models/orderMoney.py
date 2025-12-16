from models.model import Model

class OrderMoneyTransaction(Model):
    

    def get_table(self):
        return "order_money_transactions"