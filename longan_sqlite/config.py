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
    'like': 'like',
}


class SqlConfig:
    SELECT_ALL = 'SELECT * FROM {}'
    SELECT_CONDITION = 'SELECT * FROM {} WHERE {}'

    INSERT = "INSERT OR IGNORE INTO {} ({}) VALUES({})"

    UPDATE = "UPDATE {} SET {} WHERE {}"

    DELETE = "DELETE FROM {} WHERE {}"

    TABLE_INFO = "SELECT * FROM sqlite_master WHERE type='table' and name like '{}'"
