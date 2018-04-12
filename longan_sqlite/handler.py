import sqlite3


class DBHandler:
    _connect = None
    _cursor = None

    @staticmethod
    def init(db_path):
        DBHandler._connect = sqlite3.connect(db_path)
        DBHandler._cursor = DBHandler._connect.cursor()

    @staticmethod
    def execute(sql):
        DBHandler._cursor.execute(sql)
        return DBHandler._cursor.fetchall()

    @staticmethod
    def commit():
        DBHandler._connect.commit()

    @staticmethod
    def close():
        DBHandler._cursor.close()
        DBHandler._connect.close()

    @staticmethod
    def desc():
        return DBHandler._cursor.description

    @staticmethod
    def affect():
        return DBHandler._cursor.rowcount

    @staticmethod
    def last_id():
        return DBHandler._cursor.lastrowid
