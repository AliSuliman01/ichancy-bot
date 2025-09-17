from abc import ABC, abstractmethod

from database import Database

class Model(ABC):
    def __init__(self):
        self.table = self.get_table()

    @abstractmethod
    def get_table(self):
        pass

    def getById(self, id: int):
        self.db = Database.getConnection()
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table} WHERE id = {id}")
        items = cursor.fetchone()
        self.db.close()
        return items

    def getBy(self, conditions: dict):
        self.db = Database.getConnection()
        print(self.db)
        cursor = self.db.cursor(dictionary=True)
        where_clause = ' AND '.join([f"{k} {op}" + " %s "  for k, (op, v) in conditions.items()]) 
        sql = f"SELECT * FROM {self.table} WHERE {where_clause}"
        values = [v for k, (op, v) in conditions.items()]
        cursor.execute(sql, values)
        items = cursor.fetchall()
        self.db.close()
        return items

    def getAll(self):
        self.db = Database.getConnection()
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table}")
        items = cursor.fetchall()
        self.db.close()
        return items

    def insert(self, data: dict):
        self.db = Database.getConnection()
        cursor = self.db.cursor(dictionary=True)
        print(f"INSERT INTO {self.table} ({', '.join(data.keys())} ) VALUES(" + ', '.join(f"'{value}'" if isinstance(value , str) else f"{value}" for value in data.values() ) + ")")
        cursor.execute(f"INSERT INTO {self.table} ({', '.join(data.keys())} ) VALUES(" + ', '.join(f"'{value}'" if isinstance(value , str) else f"{value}" for value in data.values() ) + ")")
        self.db.commit()
        self.db.close()
    def update(self, conditions: dict, data: dict):
        """
        conditions: dict of {key: (operator, value)}, e.g. {'id': ('=', 5), 'name': ('LIKE', '%foo%')}
        data: dict of {column: value}
        """
        self.db = Database.getConnection()
        cursor = self.db.cursor(dictionary=True)
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} {op} %s" for k, (op, v) in conditions.items()])
        sql = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
        values = list(data.values()) + [v for k, (op, v) in conditions.items()]
        cursor.execute(sql, values)
        self.db.commit()
        self.db.close()