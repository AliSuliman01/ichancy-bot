from abc import ABC, abstractmethod

from database import Database

class Model(ABC):
    def __init__(self , cursor):
        self.table = self.get_table()
        self.cursor = cursor
    @abstractmethod
    def get_table(self):
        pass

    def getById(self, id: int):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = {id}")
        items = self.cursor.fetchone()
        return items

    def getBy(self, conditions: dict):
        where_clause = ' AND '.join([f"{k} {op}" + " %s "  for k, (op, v) in conditions.items()]) 
        sql = f"SELECT * FROM {self.table} WHERE {where_clause}"
        values = [v for k, (op, v) in conditions.items()]
        self.cursor.execute(sql, values)    
        items = self.cursor.fetchall()
        return items

    def getAll(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        items = self.cursor.fetchall()
        return items

    def insert(self, data: dict):
        self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(data.keys())} ) VALUES(" + ', '.join(f"'{value}'" if isinstance(value , str) else f"{value}" for value in data.values() ) + ")")
    def update(self, conditions: dict, data: dict):
        """
        conditions: dict of {key: (operator, value)}, e.g. {'id': ('=', 5), 'name': ('LIKE', '%foo%')}
        data: dict of {column: value}
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} {op} %s" for k, (op, v) in conditions.items()])
        sql = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
        values = list(data.values()) + [v for k, (op, v) in conditions.items()]
        self.cursor.execute(sql, values)
