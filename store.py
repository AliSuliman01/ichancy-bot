import mysql.connector
import config.database
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
                    status VARCHAR(255) NOT NULL,
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
                    transfeer_num VARCHAR(255),
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
                    transfeer_num VARCHAR(255),
                    user_id INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS sham_cash_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfeer_num VARCHAR(255),
                    user_id INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    action_type VARCHAR(255) NOT NULL,
                    value INT NULL,
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
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages_to_admin (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       user_id INT NOT NULL,
                       message TEXT NOT NULL,
                       photo TEXT NULL,
                       reply TEXT NULL,
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

initializeDatabase()