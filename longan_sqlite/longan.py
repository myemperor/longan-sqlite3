from .handler import DBHandler
from .config import *
from .util import *


class Longan:
    """
    此类的目的是对数据库访问进行一层包装
    查询：     md.select().from_table().where().query()
    插入或修改：md.from_table().insert_or_update(Field())
    删除：     md.where(age_lt=50).delete()
              md.delete(field_obj)
    """
    db_path = None

    @staticmethod
    def init(db_path, debug=False):
        Longan.db_path = db_path
        DBHandler.init(db_path, debug)

    def __init__(self, table_name=None):
        """
        仅提供初始化，处理表 的操作
        :param table_name: 待处理的表
        """
        if not Longan.db_path:
            raise RuntimeError("Please init db_path first!")
        if table_name:
            self.from_table(table_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DBHandler.close()

    def from_table(self, table_name):
        """
        设置需要处理的表
        :param table_name: 待处理的表
        :return: BaseModel
        """
        self._table_name = table_name
        self._key = None
        self.clear()
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
            opt = opt_map[k[index + 1:]]
            v = add_quotes(v)
            if opt == 'IN':
                v = "({})".format(", ".join([add_quotes(x) for x in v]))
            if opt == 'BETWEEN':
                v = "{} AND {}".format(add_quotes(v[0]), add_quotes(v[-1]))
            condition.append("{} {} {}".format(field, opt, str(v)))
        self._condition = ' and '.join(condition)
        return self

    def query(self):
        """
        查询语句
        新支持分组聚合
        :return: Filed
        """
        # 默认选择所有字段
        sql = SqlConfig.SELECT
        if self._aggregate:
            sql = sql.replace('*', self._aggregate)
        if self._condition:
            sql += SqlConfig.WHERE
        if self._group_field:
            sql += SqlConfig.GROUP_BY
        if self._ignore_case:
            sql += self._ignore_case
        sql = sql.format(self._table_name, self._condition, self._group_field)
        ret = DBHandler.execute(sql)
        self.clear()
        field_arr = [field[0] for field in DBHandler.desc()]
        return convert_dicts(field_arr, ret)

    def insert_or_update(self, *field_obj):
        """
        插入或更新
        :param field_obj: Filed
        :return:
        """
        insert_sql_0 = SqlConfig.INSERT
        for obj in field_obj:
            insert_sql = insert_sql_0.format(self._table_name, obj.keys_str(), obj.values_str())
            DBHandler.execute(insert_sql)
            key = self.primary_key()
            if DBHandler.affect() == 0:
                update_sql = SqlConfig.UPDATE
                value = obj.join('=')
                where = "{}={}".format(key, obj.get(key))
                update_sql = update_sql.format(self._table_name, value, where)
                DBHandler.execute(update_sql)
            else:
                obj.set(key, DBHandler.last_id(), force=False)
        DBHandler.commit()

    def delete(self, field_obj=None):
        """
        删除操作，可以和where语句，或field交替使用
        md.where(age_lt=50).delete()
        md.delete(field_obj)
        :param field_obj: Filed
        :return: 0 or 1
        """
        sql = SqlConfig.DELETE
        if field_obj:
            key = self.primary_key()
            if not field_obj.get(key):
                return 0
            where = "{}={}".format(key, field_obj.get(key))
            sql = sql.format(self._table_name, where)
        else:
            if not self._condition:
                return 0
            sql = sql.format(self._table_name, self._condition)
        DBHandler.execute(sql)
        self.clear()
        DBHandler.commit()
        return DBHandler.affect()

    def primary_key(self):
        """
        通过sql语句获取当前表的主键
        :return:
        """
        if self._key:
            return self._key
        sql = SqlConfig.TABLE_INFO.format(self._table_name)
        table_info = DBHandler.execute(sql)[0]
        create_sql = table_info[4]
        start = create_sql.find('(') + 1
        end = create_sql.rfind(')')
        column_list = create_sql[start:end].split(',')
        for column in column_list:
            column = column.strip()
            if 'PRIMARY KEY' in column.upper():
                if '(' in column:
                    start = column.find('(') + 1
                    end = column.rfind(')')
                    key = column[start:end].strip()
                else:
                    key = column[:column.find(' ') + 1]
                self._key = key.strip()
                return self._key

    def group_by(self, field):
        self._group_field = field
        return self

    def aggregate(self, **kwargs):
        """
        聚合函数
        格式如下：   字段名_聚合函数名="别名"
                    如果别名为空字符串，则默认别名为：字段名_聚合函数名
        :param kwargs: age_max="maxAge"
        :return:
        """
        aggr_list = []
        for k, v in kwargs.items():
            index = k.find('_')
            field = k[:index]
            aggr = k[index + 1:]
            if aggr in aggr_opt_map:
                v = v if v else k
                sql = "{}({}) {}".format(aggr_opt_map[aggr], field, v)
                aggr_list.append(sql)
        self._aggregate = ','.join(aggr_list)
        return self

    def ignore_case(self, ignore=True):
        if ignore:
            self._ignore_case = " COLLATE NOCASE "
        else:
            self._ignore_case = None
        return self

    def clear(self):
        self._condition = None
        self._group_field = None
        self._group_opt = None
        self._aggregate = None
        self._ignore_case = None

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
        :param sql_path:
        :return:
        """
        with open(sql_path) as f:
            return DBHandler.execute(f.read())
