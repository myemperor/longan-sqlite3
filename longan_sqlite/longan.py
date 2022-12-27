from .handler import DBHandler
from .config import *
from .util import *
from .kernel import Kernel
import os


class Longan:
    """
    此类的目的是对数据库访问进行一层包装
    查询：     md.select().from_table().where().query()
    插入或修改：md.from_table().insert_or_update(Field())
    删除：     md.where(age_lt=50).delete()
              md.delete(field_obj)
    """
    db_path = None
    db_handler = None

    @staticmethod
    def init(db_path, debug=False):
        abspath = os.path.abspath(db_path)
        if Longan.db_path != abspath:
            Longan.db_path = os.path.abspath(db_path)
            Longan.db_handler = DBHandler(db_path, debug)

    def __init__(self, table_name=None):
        """
        仅提供初始化，处理表 的操作
        :param table_name: 待处理的表
        :type  table_name: str
        """
        if not Longan.db_path:
            raise RuntimeError("Please init db_path first!")
        if table_name:
            self.from_table(table_name)
        else:
            self.clear()

    def __exit__(self, exc_type, exc_val, exc_tb):
        Longan.db_handler.close()

    def from_table(self, table_name):
        """
        设置需要处理的表
        :param table_name: 待处理的表
        """
        self._table_name = table_name
        self._primary_key = None
        self._fields = None
        self.clear()
        return self

    def where(self, **kwargs):
        """
        提供where语句的封装：
        如：md.where(age_gt=5,name_like='m%') = "WHERE age > 5 and name like 'm%'"
        :param kwargs: 字典
        """

        condition = []
        for k, v in kwargs.items():
            index = k.rfind('_')
            field = k[:index]
            opt = opt_map[k[index + 1:]]
            v = add_quotes(v)
            if opt == 'IN':
                if not isinstance(v, tuple):
                    raise RuntimeError("Opt(IN) value must be tuple!")
                v = "({})".format(", ".join([add_quotes(x) for x in v]))
            if opt == 'BETWEEN':
                if not isinstance(v, tuple):
                    raise RuntimeError("Opt(BETWEEN) value must be tuple!")
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
        if self._order_by:
            sql += self._order_by
        if self._limit:
            sql += self._limit

        sql = sql.format(self._table_name, self._condition, self._group_field)
        ret = Longan.db_handler.execute(sql)
        self.clear()
        field_arr = [field[0] for field in Longan.db_handler.desc()]
        return convert_dicts(field_arr, ret)

    def insert_or_update(self, *field_obj):
        """
        插入或更新
        :param field_obj: Filed
        :return:
        """
        key = self.primary_key()
        for obj in field_obj:
            if obj.get(key):
                update_sql = SqlConfig.UPDATE
                value = obj.join('=')
                where = "{}={}".format(key, add_quotes(obj.get(key)))
                update_sql = update_sql.format(self._table_name, value, where)
                Longan.db_handler.execute(update_sql)
            else:
                insert_sql = SqlConfig.INSERT.format(self._table_name, obj.keys_str(), obj.values_str())
                Longan.db_handler.execute(insert_sql)
                obj.set(key, Longan.db_handler.last_id(), force=False)
        Longan.db_handler.commit()

    def insert(self, *field_obj):
        """
        插入
        :param field_obj: Filed
        :return:
        """
        key = self.primary_key()
        for obj in field_obj:
            insert_sql = SqlConfig.INSERT.format(self._table_name, obj.keys_str(), obj.values_str())
            Longan.db_handler.execute(insert_sql)
            obj.set(key, Longan.db_handler.last_id(), force=False)
        Longan.db_handler.commit()

    def update(self, *field_obj):
        """
        更新
        :param field_obj: Field
        :return:
        """
        key = self.primary_key()
        for obj in field_obj:
            update_sql = SqlConfig.UPDATE
            value = obj.join('=')
            where = "{}={}".format(key, add_quotes(obj.get(key)))
            update_sql = update_sql.format(self._table_name, value, where)
            Longan.db_handler.execute(update_sql)
        Longan.db_handler.commit()

    def delete(self, field_obj=None):
        """
        删除操作，可以和where语句，或field交替使用
        md.where(age_lt=50).delete()
        md.delete(field_obj)
        :param field_obj: Filed
        :type  field_obj: Flesh
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
        Longan.db_handler.execute(sql)
        self.clear()
        Longan.db_handler.commit()
        return Longan.db_handler.affect()

    def primary_key(self):
        """
        通过sql语句获取当前表的主键
        :return:
        """
        if not self._primary_key:
            fields = self.all_fields()
            for f in fields:
                if f.primary == 1:
                    self._primary_key = f.name
                    break
        return self._primary_key

    def all_fields(self):
        """
        通过sql语句获取当前表的所有键
        :return:
        """
        if not self._fields:
            sql = SqlConfig.TABLE_INFO.format(self._table_name)
            fields = Longan.db_handler.execute(sql)
            for f in fields:
                self._fields.append(Kernel(f))
        return self._fields

    def group_by(self, field):
        """
        分组
        :param field: 字段名称
        :type  field: str
        :return:
        """
        self._group_field = field
        return self

    def aggregate(self, **kwargs):
        """
        聚合函数
        格式如下：   字段名_聚合函数名="别名"
                    如果别名为空字符串，则默认别名为：字段名_聚合函数名
                    如果不需要使用函数，则直接使用：字段名="别名" 即可
        :param kwargs: age_max="maxAge"
        :return:
        """
        aggr_list = []
        for k, v in kwargs.items():
            index = k.rfind('_')
            sql = ""
            v = v if v else k
            if index != -1:
                field = k[:index]
                aggr = k[index + 1:]
                if aggr in aggr_opt_map:
                    sql = "{}({}) {}".format(aggr_opt_map[aggr], field, v)
            else:
                sql = v
            aggr_list.append(sql)
        self._aggregate = ','.join(aggr_list)
        return self

    def ignore_case(self, ignore=True):
        """
        是否忽略大小写
        :param ignore: 是否
        :type  ignore: bool
        :return: Longan
        """
        if ignore:
            self._ignore_case = " COLLATE NOCASE "
        else:
            self._ignore_case = None
        return self

    def limit(self, limit, offset=0):
        """
        分页
        :param limit: 数量
        :param offset: 位置

        :type  limit: int
        :type  offset: int
        """
        if limit == None or limit < 1:
            raise RuntimeError("Limit must greater than 0")
        if offset < 0:
            raise RuntimeError("Offset must be positive")
        self._limit = SqlConfig.LIMIT.format(limit, offset)
        return self

    def order_by(self, key, desc=False):
        """
        排序
        :param key:  字段名称
        :param desc: 顺序
        :return: self
        :rtype Longan
        """
        order = "DESC" if desc else "ASC"
        self._order_by = SqlConfig.ORDER_BY.format(key, order)
        return self

    def field(self, name=None, type=None, not_null=False, default=None, unique=None
              , primary_key=False, check=None, length=0, increment=False):
        """
        创建一个表格时使用，用于生成单个字段

        :param name:        字段名称
        :param type:        字段类型
        :param not_null:    是否可以为null
        :param default:     默认值
        :param unique:      是否唯一
        :param primary_key: 是否为主键
        :param check:       值的范围  start_end   如：大于5(5), 小于10(_10), 介于5-10之间(5_10)
        :param length:      字段类型的长度，当类型为字符串时，需要显示的指定
        :param increment:   自增

        :type name          str
        :type type          str
        :type not_null      bool
        :type unique        bool
        :type primary_key   bool
        :type check:        str
        :type length:       int
        :type increment:    bool
        :return: self
        """
        if not name or not type:
            raise RuntimeError("need param!")
        type = type.upper()
        if FieldType.CHAR in type and length <= 0:
            raise RuntimeError("Char type need init length！")
        if length:
            type = "{}({})".format(type, length)

        row = [name, type]
        if not_null:
            row.append(FieldAttr.NOT_NULL)
        if default:
            row.append(FieldAttr.DEFAULT + " " + add_quotes(default))
        if unique:
            row.append(FieldAttr.UNIQUE)
        if primary_key:
            row.append(FieldAttr.PRIMARY_KEY)
        if increment and type == FieldType.INTEGER and primary_key:
            row.append(FieldAttr.AUTOINCREMENT)
        if check:
            check_list = check.split("_")
            check = ""
            if check_list[0]:
                check = name + ">" + check_list[0]
            if check_list[1]:
                if check:
                    check += " AND "
                check += name + "<" + check_list[1]
            row.append(FieldAttr.CHECK.format(check))
        self._field_row.append(" ".join(row))
        return self

    def create_table(self, table_name=None, force=False):
        """
        创建一张表
        :param table_name:  表名
        :param force:       是否强制创建
        """
        if not self._field_row:
            raise RuntimeError("please create field first!")
        if not table_name:
            raise RuntimeError("Need table name")
        sql = SqlConfig.CREAT_TABLE_FORCE if force else SqlConfig.CREAT_TABLE
        sql = sql.format(table_name.upper(), ",\n\t".join(self._field_row))
        Longan.db_handler.execute(sql)
        self.clear()
        Longan.db_handler.commit()
        self.from_table(table_name)

    def clear(self):
        self._primary_key = None
        self._fields = []
        self._condition = None
        self._group_field = None
        self._group_opt = None
        self._aggregate = None
        self._ignore_case = None
        self._limit = None
        self._order_by = None
        self._field_row = []

    @staticmethod
    def close():
        Longan.db_handler.close()

    @staticmethod
    def execute(sql):
        """
        直接执行sql语句，不推荐使用
        :param sql:
        :return:
        """
        return Longan.db_handler.execute(sql)

    @staticmethod
    def execute_file(sql_path):
        """
        直接执行sql语句，不推荐使用
        :param sql_path:
        :return:
        """
        with open(sql_path) as f:
            for sql in f.read().split(';'):
                Longan.db_handler.execute(sql)
