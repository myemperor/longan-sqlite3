from longan_sqlite import Longan, Flesh

# 初始化Longan，指定数据库地址
# debug为true，则打印所有sql语句
Longan.init('test.db', debug=True)

# 指定某张表实例化longan
longan = Longan('company')

# 执行sql文件
longan.execute_file('company.sql')

# 批量插入或修改
flesh_list = [
    Flesh(name='jobs', age=50, address='America', salary=90),
    Flesh(name='杰克马', age=45, address='china', salary=70),
    Flesh(name='黄鹤', age=32, address='china', salary=2),
    Flesh(name='baby', age=4, address='china', salary=-5),
    Flesh(name='金三瘦', age=35, address='朝鲜', salary=900)
]
longan.insert_or_update(*flesh_list)

# 单独插入
flesh = Flesh(name='emperor', age=23, address='北京', salary=10)
longan.insert_or_update(flesh)
# 涨薪了
flesh.salary += 5
longan.insert_or_update(flesh)

# 插入或更新的单独接口
# 1.1
flesh = Flesh(name='picker', age=33, address='北京', salary=30)
longan.insert(flesh)
# 裁员
flesh.salary -= 5
longan.update(flesh)

# 查询
# 0.5 where子句 新增 between 和 in 的支持
#              like可以忽略大小写
ret = longan.ignore_case() \
    .where(age_gt=5, name_like="%JOB%",
           salary_between=(50, 100),
           address_in=('America', 'china', '朝鲜')).query()
for r in ret:
    print(r)
    if r.name == 'jobs':
        pass
        # 通过对象进行删除
        # longan.delete(r)

# 0.3新增分组聚合查询
# 0.6支持选择其他字段，但和多个返回结果唯一的聚合函数一起使用时，结果可能出乎意料
# longan.aggregate(age_max="maxAge", salary_min="minSalary", id="ID")
longan.aggregate(name_upper="upperName", id="", salary="")

# 0.6新增排序和分页
longan.order_by("id", desc=True)
longan.limit(2, 2)
# longan.where(age_gt=5)
# longan.group_by('address')
ret = longan.query()
for r in ret:
    print(r)
# ret = longan.where(age_gt=5).query()

# 通过条件进行删除
longan.where(id_gt=0).delete()

longan.primary_key()
