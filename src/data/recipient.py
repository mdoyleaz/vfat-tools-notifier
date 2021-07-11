from src.data.database import Database

class Recipient(Database):
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.data = {
            'email': email,
            'name': name
            }

        Database.__init__(self, table='recipients') 
    
    def get(self):
        return


recipients = Recipient(name='michael', email='example@example.com').create()
print(recipients)
