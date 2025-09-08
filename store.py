import mysql.connector
def createTheDatabase():
    mydb = mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "",
    )
    cursor = mydb.cursor()



    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ccipdatabase")
    except: 
        print("the database is exists")
    cursor.execute("""USE ccipdatabase""")

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


def insertNewUser(telegram_id, telegram_username = None):

    mydb = mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "",
        database = "ccipdatabase"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT telegram_id FROM users")
    telegram_ides = cursor.fetchone()
    
    if telegram_ides is None:
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

    mydb = mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "",
        database = "ccipdatabase"
    )
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