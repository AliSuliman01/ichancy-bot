from models.model import Model

class CryptoTransaction(Model):
    

    def get_table(self):
        return "crypto_transactions"