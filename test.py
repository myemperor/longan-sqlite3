from longan_sqlite import Longan, Flesh

longan = Longan('test.db', 'company')
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

# 查询
ret = longan.where(age_gt=5).query()
for r in ret:
    print(r)
    if r.name == 'jobs':
        # 通过对象进行删除
        longan.delete(r)

# 0.3新增分组聚合查询
longan.aggregate(age_max="maxAge", salary_min="minSalary")
longan.where(age_gt=5)
longan.group_by('address')
ret = longan.query()
for r in ret:
    print(r)
# ret = longan.where(age_gt=5).query()



# 通过条件进行删除
longan.where(id_gt=0).delete()

longan.primary_key()
