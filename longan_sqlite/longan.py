from .handler import DBHandler
from .flesh import Flesh


class Longan:
    """
    此类的目的是对数据库访问进行一层包装
    查询：     md.select().from_table().where().query()
    插入或修改：md.from_table().insert_or_update(Field())
    删除：     md.where(age_lt=50).delete()
              md.delete(field_obj)
    """

    '''
    此表是为了对where语句进行匹配
    如：md.where(age_gt=5) = "WHERE age > 5"
    '''
    opt_map = {
        'gt': '>',
        'lt': '<',
        'eq': '=',
        'neq': '!=',
        'egt': '>=',
        'elt': '<=',
        'like': 'like',
    }

    def __init__(self, db_path, table_name):
        """
        仅提供初始化，处理表 的操作
        :param table_name: 待处理的表
        """
        self._table_name = table_name
        self._condition = None
        self._db_path = db_path
        DBHandler.init(db_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DBHandler.close()

    def from_table(self, table_name):
        """
        设置需要处理的表
        :param table_name: 待处理的表
        :return: BaseModel
        """
        self._table_name = table_name
        return self

    def where(self, **kwargs):
        """
        提供where语句的封装：
        如：md.where(age_gt=5,name_like='m%') = "WHERE age > 5 and name like 'm%'"
        :param kwargs: 字典
        :return: BaseModel
        """

        condition = []
        for k, v in kwargs.items():
            index = k.find('_')
            field = k[:index]
            opt = Longan.opt_map[k[index + 1:]]
            if isinstance(v, str):
                v = '"{}"'.format(v)
            condition.append("{} {} {}".format(field, opt, str(v)))
        self._condition = ' and '.join(condition)
        return self

    def query(self):
        """
        查询语句
        :return: Filed
        """
        sql = 'SELECT * FROM {}'
        if self._condition:
            sql = 'SELECT * FROM {} WHERE {}'
        sql = sql.format(self._table_name, self._condition)
        cursor = DBHandler.execute(sql)
        self._condition = None
        field_arr = [field[0] for field in cursor.description]
        return Longan.convert_dicts(field_arr, cursor.fetchall())

    def insert_or_update(self, *field_obj):
        """
        插入或更新
        :param field_obj: Filed
        :return:
        """
        insert_sql_0 = "INSERT OR IGNORE INTO {} ({}) VALUES({})"
        for obj in field_obj:
            insert_sql = insert_sql_0.format(self._table_name, obj.keys_str(), obj.values_str())
            cursor = DBHandler.execute(insert_sql)
            if cursor.rowcount == 0:
                update_sql = "UPDATE {} SET {} WHERE id={}"
                update_sql = update_sql.format(self._table_name, obj.join('='), obj.id)
                DBHandler.execute(update_sql)
            else:
                obj.id = cursor.lastrowid
        DBHandler.commit()

    def delete(self, field_obj=None):
        """
        删除操作，可以和where语句，或field交替使用
        md.where(age_lt=50).delete()
        md.delete(field_obj)
        :param field_obj: Filed
        :return: 0 or 1
        """
        sql = "DELETE FROM {} WHERE {}"
        if field_obj:
            if not field_obj.id:
                return 0
            sql = sql.format(self._table_name, "id={}".format(field_obj.id))
        else:
            if not self._condition:
                return 0
            sql = sql.format(self._table_name, self._condition)
        cursor = DBHandler.execute(sql)
        self._condition = None
        DBHandler.commit()
        return cursor.rowcount

    @staticmethod
    def close():
        DBHandler.close()

    @staticmethod
    def execute(sql):
        """
        直接执行sql语句，不推荐使用
        :param sql:
        :return:
        """
        return DBHandler.execute(sql)

    @staticmethod
    def execute_file(sql_path):
        """
        直接执行sql语句，不推荐使用
        :param sql:
        :return:
        """
        with open(sql_path) as f:
            return DBHandler.execute(f.read())

    @staticmethod
    def convert_dicts(fields, items):
        """
        :param fields:
        :param items:
        :return: list(Flesh)
        :rtype: list
        """
        ret_items = []
        for i in items:
            item_dict = {}
            for k, v in enumerate(fields):
                item_dict[v] = i[k]
            ret_items.append(Flesh(item_dict))
        return ret_items
