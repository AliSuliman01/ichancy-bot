from abc import ABC, abstractmethod

from database import Database

class Model(ABC):
    def __init__(self):
        self.db = Database.getConnection()
        self.table = self.get_table()

    @abstractmethod
    def get_table(self):
        pass

    def getById(self, id: int):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.table} WHERE id = {id}")
        return cursor.fetchone()

    def getBy(self, conditions: dict):
        cursor = self.db.cursor()
        where_clause = ' AND '.join([f"{k} {op} %s" for k, (op, v) in conditions.items()])
        sql = f"SELECT * FROM {self.table} WHERE {where_clause}"
        values = [v for k, (op, v) in conditions.items()]
        cursor.execute(sql, values)
        return cursor.fetchall()

    def getAll(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.table}")
        return cursor.fetchall()

    def insert(self, data: dict):
        cursor = self.db.cursor()
        cursor.execute(f"INSERT INTO {self.table} ({', '.join(data.keys())}) VALUES ({', '.join(data.values())})")

    def update(self, conditions: dict, data: dict):
        """
        conditions: dict of {key: (operator, value)}, e.g. {'id': ('=', 5), 'name': ('LIKE', '%foo%')}
        data: dict of {column: value}
        """
        cursor = self.db.cursor()
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} {op} %s" for k, (op, v) in conditions.items()])
        sql = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
        values = list(data.values()) + [v for k, (op, v) in conditions.items()]
        cursor.execute(sql, values)