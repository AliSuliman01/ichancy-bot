import mysql.connector
import config.database

class Database:
    _conter = 0
    _connection = None
    print(_connection)

    @staticmethod
    # def getConnection():
        
    #     if Database._connection is not None:
    #         print("Old Connection")
    #         return Database._connection

    #     try:
    #         Database._connection = mysql.connector.connect(
    #             host = config.database.host,
    #             port = config.database.port,
    #             username = config.database.username,
    #             password = config.database.password,
    #             database = config.database.databaseName
    #         )
    #         print("New Connection")
    #         return Database._connection
    #     except(Exception, mysql.connector.Error) as error: 
    #         print(f"Failed to connect to the database: {error}")

    
    def getConnection():
        
        try:
            Database._conter+=1
            Database._connection = mysql.connector.connect(
                host = config.database.host,
                port = config.database.port,
                username = config.database.username,
                password = config.database.password,
                database = config.database.databaseName
            )
            print(Database._conter)
            return Database._connection
        
        except(Exception, mysql.connector.Error) as error: 
            print(f"Failed to connect to the database: {error}")
