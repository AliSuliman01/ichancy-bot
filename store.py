import mysql.connector
import config.database
from datetime import datetime
def initializeDatabase():

    try:
        mydb = getDatabaseConnection(initialize=True)
        cursor = mydb.cursor()
    

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database.databaseName}")
        
        cursor.execute(f"USE {config.database.databaseName}")

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_id VARCHAR(25) UNIQUE NOT NULL,
                    telegram_username VARCHAR(255),
                    player_id VARCHAR(255) NOT NULL,
                    name VARCHAR(255),
                    password VARCHAR(255),
                    email VARCHAR(255) UNIQUE NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    balance INT DEFAULT 0,
                    account_balance INT DEFAULT 0 
                        )""")


        cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    provider_id INT,
                    provider_type VARCHAR(255),
                    user_id INT NOT NULL,
                    value INT NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS account_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)


        cursor.execute("""
                CREATE TABLE IF NOT EXISTS bemo_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfer_num VARCHAR(255),
                    user_id INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    value INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS syriatel_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfer_num VARCHAR(255),
                    user_id INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS gifts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_goal_id VARCHAR(20) NOT NULL,
                    user_id INT NOT NULL,
                    redeemed_at DATETIME NULL,
                    code VARCHAR(25) NOT NULL,
                    ammount INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

    except(Exception, mysql.connector.Error) as error: 
        print(f"Failed to connect to the database: {error}")


def getDatabaseConnection(initialize = False):
    try:
        if not initialize:
            mydb = mysql.connector.connect(
                host = config.database.host,
                port = config.database.port,
                username = config.database.username,
                password = config.database.password,
                database = config.database.databaseName
            )
            return mydb
        else:
            mydb = mysql.connector.connect(
            host = config.database.host,
            port = config.database.port,
            username = config.database.username,
            password = config.database.password,
            )
            return mydb
    except(Exception, mysql.connector.Error) as error: 
        print(f"Failed to connect to the database: {error}")

def getTelegramIdByUserId(userId):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT telegram_id FROM users WHERE id = %s", (userId,))
    telegram_ids = cursor.fetchone()
    return telegram_ids[0] if telegram_ids else None

def getUserById(userId):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
    return cursor.fetchone()

def getUserByTelegramId(telegram_id):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
    return cursor.fetchone()

def getUserIdByTelegramId(telegram_id):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
    return cursor.fetchone()

def insertGift(telegram_id , giftAmmount , telegram_goal_id , code):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    user = getUserByTelegramId(telegram_id)
    balance = user.get('balance') - int(giftAmmount)
    if balance < 0:
        mydb.close()
        return False
    sqlInsert = """
    UPDATE users SET balance = %(balance)s WHERE telegram_id = %(telegram_id)s
    """
    data = {
        'balance' : balance,
        'telegram_id':telegram_id
    }
    cursor.execute(sqlInsert, data)
    mydb.commit() 

    sqlInsert = """
                INSERT INTO gifts (telegram_goal_id , ammount , user_id , code) VALUES (%(telegram_goal_id)s, %(ammount)s , %(user_id)s , %(code)s)
            """
    data = {
            'telegram_goal_id' : telegram_goal_id ,
            'ammount' : giftAmmount,
            'user_id' : user.get('id'),
            'code' : code
        }
    cursor.execute(sqlInsert, data)
    mydb.commit()
    mydb.close()
    return True


def validateRedeemedAt(resault , cursor , mydb):
    gift_id = resault.get('id')
    sql = """
        UPDATE gifts SET redeemed_at = %(redeemed_at)s
        WHERE id = %(gift_id)s
        """
    data = {
    'gift_id': gift_id,
    'redeemed_at': datetime.now()
    }
    cursor.execute(sql,data)
    mydb.commit()


def addGiftAmmountToBalance(telegram_id , cursor , resault):
    sql = """SELECT balance FROM users WHERE telegram_id = %(telegram_id)s"""
    data = {
        'telegram_id':telegram_id,
    }
    cursor.execute(sql,data)
    newBalance = cursor.fetchone().get('balance')
    newBalance += resault.get('ammount')
    return newBalance

def insertTheNewBalance(telegram_id , cursor , resault , mydb):
    newBalance = addGiftAmmountToBalance(telegram_id , cursor , resault)
    sql = """
        UPDATE users SET balance = %(balance)s
        WHERE telegram_id = %(telegram_id)s
        """
    data = {
    'balance': newBalance,
    'telegram_id': telegram_id
    }
    cursor.execute(sql,data)
    mydb.commit()
    mydb.close()

    
def getGift(code , telegram_id):
     mydb = getDatabaseConnection()
     cursor = mydb.cursor(dictionary=True)
     sql = """SELECT * FROM users U JOIN gifts G WHERE G.user_id = U.id 
     AND G.telegram_goal_id = %(telegram_id)s AND code = %(code)s
     AND redeemed_at IS NULL"""
     data = {
         'telegram_id':telegram_id,
         'code':code
     }     
     cursor.execute(sql,data)
     resault = cursor.fetchone()
     print('nfbdbvfldvbjkfddfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
     if resault:
         validateRedeemedAt(resault , cursor , mydb)
         insertTheNewBalance(telegram_id , cursor , resault , mydb)
         return True
     return False
    
def insertNewUser(telegram_id, telegram_username = None):

    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    
    if not getUserByTelegramId(telegram_id):
        sqlInsert = """
                INSERT INTO users (telegram_id , telegram_username) VALUES (%(telegram_id)s, %(telegram_username)s)
            """
        data = {
            'telegram_id' : telegram_id,
            'telegram_username' : telegram_username 
        }
        cursor.execute(sqlInsert, data)
        mydb.commit()
    
    mydb.close()

def insertSyriatelCashTransaction(telegram_id, transfer_num, value):

    mydb = getDatabaseConnection()
    cursor = mydb.cursor(dictionary=True)
    
    user_id = getUserIdByTelegramId(telegram_id)
    sqlInsert = """
            INSERT INTO syriatel_transactions (user_id , transfer_num, value) VALUES (%(user_id)s, %(transfer_num)s, %(value)s)
        """
    data = {
        'user_id' : user_id,
        'transfer_num' : transfer_num,
        'value' : value
    }
    cursor.execute(sqlInsert, data)
    mydb.commit()
    
    mydb.close()


def insertUserDetailes(telegram_id,name,password,email,player_id):

    mydb = getDatabaseConnection()

    cursor = mydb.cursor()    
    
    sqlInsert = """
    UPDATE users SET name = %(name)s, password = %(password)s, email = %(email)s , player_id = %(player_id)s
    WHERE telegram_id = %(telegram_id)s
    """

    data = {
        'name': name,
        'password': password,
        'email': email,
        'telegram_id': telegram_id,
        'player_id': player_id
    }
    cursor.execute(sqlInsert, data)
    mydb.commit()
    mydb.close()   

initializeDatabase()