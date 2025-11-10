from models.model import Model

class MessageToAdmin(Model):
    

    def get_table(self):
        return "messages_to_admin"