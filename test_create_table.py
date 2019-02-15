from longan_sqlite import *

Longan.init('test.db', debug=True)
longan = Longan()
longan.field(name="age", type=FieldType.INT, not_null=True, default=15, primary_key=False
             , unique=False, check="10_80")
longan.field(name="name", type=FieldType.VARCHAR, not_null=True, default="xx", primary_key=True
             , unique=True, length=10)
longan.field(name="id", type=FieldType.INT, not_null=True
             , unique=True, increment=True)
longan.create_table("m_test")

flesh_list = [
    Flesh(name='jobs', age=51, id=1),
    Flesh(name='杰克马', age=52),
    Flesh(name='baby', age=53),
    Flesh(name='黄鹤', age=20),
    Flesh(name='金三瘦', age=30),
]
longan.insert_or_update(*flesh_list)

# 单独插入
flesh = Flesh(name='emperor', age=33)
longan.insert_or_update(flesh)
flesh.age += 1
longan.insert_or_update(flesh)

ret = longan.query()
for r in ret:
    print(r)
