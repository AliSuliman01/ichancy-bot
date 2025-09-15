import mysql.connector
import config.database

class Database:
    
    _connection = None
    print("############################################################")
    print("############################################################")
    print("############################################################")
    print("############################################################")
    print(_connection)
    @staticmethod
    def getConnection():
        
        if Database._connection is not None:
            return Database._connection

        try:
            Database._connection = mysql.connector.connect(
                host = config.database.host,
                port = config.database.port,
                username = config.database.username,
                password = config.database.password,
                database = config.database.databaseName
            )
            return Database._connection
        except(Exception, mysql.connector.Error) as error: 
            print(f"Failed to connect to the database: {error}")
