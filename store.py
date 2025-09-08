import mysql.connector
import config.database

def initializeDatabase():

    try:
        mydb = mydb = mysql.connector.connect(
            host = config.database.host,
            port = config.database.port,
            username = config.database.username,
            password = config.database.password,
        )

        cursor = mydb.cursor()
    

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database.databaseName}")
        
        cursor.execute(f"USE {config.database.databaseName}")

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_id INT UNIQUE NOT NULL,
                    telegram_username VARCHAR(255),
                    name VARCHAR(255),
                    password VARCHAR(255),
                    email VARCHAR(255) UNIQUE NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    balance INT,
                    account_balance INT   
                        )""")


        cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    provider_id INT,
                    provider_type VARCHAR(255),
                    user_id INT NOT NULL,
                    value INT NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)


        cursor.execute("""
                CREATE TABLE IF NOT EXISTS bemo_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfer_num VARCHAR(255),
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS syriatel_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfer_num VARCHAR(255),
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    except(Exception, mysql.connector.Error) as error: 
        print(f"Failed to connect to the database: {error}")


def getDatabaseConnection():
    try:
        mydb = mysql.connector.connect(
            host = config.database.host,
            port = config.database.port,
            username = config.database.username,
            password = config.database.password,
            database = config.database.databaseName
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

def checkTelegramIdExists(telegram_id):
    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = %s", (telegram_id,))
    telegram_ids = cursor.fetchone()
    return True if telegram_ids else False

def insertNewUser(telegram_id, telegram_username = None):

    mydb = getDatabaseConnection()
    cursor = mydb.cursor()
    
    if not checkTelegramIdExists(telegram_id):
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


def insertUserDetailes(telegram_id,name,password,email):

    mydb = getDatabaseConnection()

    cursor = mydb.cursor()    
    
    sqlInsert = """
    UPDATE users SET name = %(name)s, password = %(password)s, email = %(email)s
    WHERE telegram_id = %(telegram_id)s
    """

    data = {
        'name': name,
        'password': password,
        'email': email,
        'telegram_id': telegram_id
    }
    cursor.execute(sqlInsert, data)
    mydb.commit()
    mydb.close()   

#createTheDatabase()
#insertUserDetailes(1419197314,"fgfgf","123456","soso@gmail.com")