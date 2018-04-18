import sqlite3


class DBHandler:
    _connect = None
    _cursor = None
    _debug = False

    @staticmethod
    def init(db_path, debug=False):
        DBHandler._connect = sqlite3.connect(db_path)
        DBHandler._cursor = DBHandler._connect.cursor()
        DBHandler._debug = debug

    @staticmethod
    def execute(sql):
        if DBHandler._debug:
            print("[Longan Debug]",end='\t')
            print(sql)
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
