"""
此表是为了对where语句进行匹配
如：md.where(age_gt=5) = "WHERE age > 5"
"""
opt_map = {
    'gt': '>',
    'lt': '<',
    'eq': '=',
    'neq': '!=',
    'egt': '>=',
    'elt': '<=',
    'like': 'LIKE',
    'in': 'IN',
    'between': 'BETWEEN',
    'exists': 'EXISTS',
}

aggr_opt_map = {
    'sum': 'SUM',
    'avg': 'AVG',
    'max': 'MAX',
    'min': 'MIN',
    'abs': 'ABS',
    'upper': 'UPPER',
    'lower': 'LOWER',
    'count': 'COUNT',
    'length': 'LENGTH',
}


class FieldType:
    INT = 'INT'
    INTEGER = "INTEGER"
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    NCHAR = "NCHAR"
    NVACHAR = "NVACHAR"
    TEXT = "TEXT"
    BLOB = "BLOB"
    REAL = "REAL"
    DOUBLE = "DOUBLE"
    FLOAT = "FLOAT"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    DATETIME = "DATETIME"


class FieldAttr:
    NOT_NULL = "NOT NULL"
    DEFAULT = "DEFAULT"
    UNIQUE = "UNIQUE"
    PRIMARY_KEY = "PRIMARY KEY"
    AUTOINCREMENT = "AUTOINCREMENT"
    CHECK = "CHECK({})"


class SqlConfig:
    SELECT = 'SELECT * FROM {}'
    INSERT = "INSERT OR IGNORE INTO {} ({}) VALUES({})"
    UPDATE = "UPDATE {} SET {} WHERE {}"
    DELETE = "DELETE FROM {} WHERE {}"
    TABLE_INFO = "PRAGMA TABLE_INFO({})"

    WHERE = " WHERE {} "
    GROUP_BY = " GROUP BY {} "
    ORDER_BY = " ORDER BY {} {}"
    LIMIT = " LIMIT {} OFFSET {} "

    CREAT_TABLE = "\nCREATE TABLE IF NOT EXISTS {}(\n\t{}\n);"
    CREAT_TABLE_FORCE = "\nCREATE TABLE {}(\n\t{}\n);"
