from database import Database

db = Database.getConnection()
db1 = Database.getConnection()
db.start_transaction()

print(db)
print(db1)


db.commit()

db.close()
