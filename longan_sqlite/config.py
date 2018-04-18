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
}

aggr_opt_map = {
    'sum': 'SUM',
    'avg': 'AVG',
    'max': 'MAX',
    'min': 'MIN',
    'count': 'COUNT',
}


class SqlConfig:
    SELECT = 'SELECT * FROM {}'
    INSERT = "INSERT OR IGNORE INTO {} ({}) VALUES({})"
    UPDATE = "UPDATE {} SET {} WHERE {}"
    DELETE = "DELETE FROM {} WHERE {}"
    TABLE_INFO = "SELECT * FROM sqlite_master WHERE type='table' and name like '{}'"

    WHERE = " WHERE {} "
    GROUP_BY = " GROUP BY {} "
