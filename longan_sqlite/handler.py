import sqlite3
import logging


class DBHandler:

    def __init__(self, db_path, debug=False, logger=None):
        self._debug = debug
        self._connect = sqlite3.connect(db_path, check_same_thread=False)
        self._cursor = self._connect.cursor()
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            logger.addHandler(console_handler)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            console_handler.setFormatter(formatter)
        self._logger = logger

    def execute(self, sql):
        if self._debug:
            self._logger.info("[Longan Debug] {}".format(sql))
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def commit(self):
        self._connect.commit()

    def close(self):
        self._cursor.close()
        self._connect.close()

    def desc(self):
        return self._cursor.description

    def affect(self):
        return self._cursor.rowcount

    def last_id(self):
        return self._cursor.lastrowid
