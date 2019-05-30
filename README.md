<font style='font-family:Courier New '>

# 欢迎使用longan-sqlite3 v1.0 
------

我们理解您需要更便捷更高效更轻量级的工具记录数据，并将其中承载的价值传播给他人，**longan-sqlite3** 是我们给出的答案 ———— 让您随心所欲的完成如下功能

**Python version >= 3.6**
> * Create
> * Research
> * Update
> * Delete

![longan-sqlite3-logo](https://img-blog.csdn.net/20180329103235613)



> 您现在看到的这个 longan-sqlite3 版本，为正式版，以发布至pypi

> 1.0 正式发布至pypi

> 0.8 修复获取表主键的方式，并增加了 Kernel 和 FastFlesh 以简化操作

> 0.7 新增创建表

> 0.6 新增排序和分页的函数，支持了几乎所有聚合函数

> 0.5 where子句
>       1.新增 between 和 in 的支持, 新增方法；
>       2.提供like表达式忽略大小写的功能
>     init方法提供debug模式，可以打印sql语句

> 0.4 新增API文档

> 0.3 新增分组聚合函数

> 0.2 修复了主键判断，修复了handler接口
------

## 什么是 longan

longan 是一种水果，很甜，喜欢的人吃很多，不喜欢的人一吃就上火！

### 1. 以下是我们计划中的功能 

- [x] 支持 CRUD
- [x] 支持 分组聚合函数
- [x] 修复 API文档
- [x] 新增 where 语句支持

### 2. 以下是我们的行为守恒公式

longan=mc^2

### 3. 使用方法

 - 安装
```shell
pip install longan_sqlite
```

 - 导入longan
```python
from longan_sqlite import Longan, Flesh
```
 - 初始化longan
```python
Longan.init('test.db', True)
```
 - 实例化longan
```python
longan = Longan('company')
```
 - 导入数据库（此处会在日后的版本中进行抽象）
```python
longan.execute_file('company.sql')
```
 - 其中的表结构 company.sql
```sql
CREATE TABLE IF NOT EXISTS COMPANY(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name           TEXT    NOT NULL,
   age            INT     NOT NULL,
   address        CHAR(50),
   salary         REAL
);
```
 - Create
```python
flesh = Flesh(name='emperor', age=23, address='北京', salary=10)
longan.insert_or_update(flesh)
```
 - Update
```python
flesh.age += 1
flesh.salary += 5
longan.insert_or_update(flesh)
```
 - Query
```python
ret = longan.where(age_gt=18, salary_elt=100, salary_gt=0).query()
for r in ret:
    print(r)
```
 - Delete
```python
# 查询
ret = longan.where(age_gt=18, salary_elt=100, salary_gt=0).query()

for r in ret:
    print(r)
    if r.name == 'jobs':
        # 通过对象进行删除
        longan.delete(r)

# 通过条件进行删除
longan.where(id_gt=0).delete()
```
 - 0.3新增分组聚合查询
```python
longan.aggregate(age_max="maxAge", salary_min="minSalary")
longan.where(age_gt=5)
longan.group_by('address')
ret = longan.query()
for r in ret:
    print(r)
```
### 4. API文档

| 接口        | 参数   |  说明  |
| :--------:   | :-----:  | :----  |
| init | db_path, debug | 初始化数据库文件，开启debug模式后，将会打印sql语句 |
| select     | - |   未开放，当前版本默认为选择全部字段，除非使用聚合函数     |
| from_table | table_name | 指定查询表 |
| where | **field_condition | 借鉴了Django中查询的操作，"_"前为字段名，后为表达式，需要传递值 |
| insert_or_update | *field_obj | 将一个或多个Flesh对象插入或更新到表中，会自动为对象添加主键 |
| insert | *field_obj | 将一个或多个Flesh对象插入到表中，会自动为对象添加主键 |
| update | *field_obj | 将一个或多个Flesh对象更新到表中|
| delete | *field_obj | 可以通过where方法来根据条件来进行删除，也可以对一个或多个Flesh对象直接删除，前提是对象拥有主键 |
| group_by | field | 对指定字段进行分组 |
| aggregate | **field_condition | 可以参考where语句：字段名_**聚合函数名**="别名" |
| query | - | 查询，需要组合使用 |
| primary_key | - | 主键 |
| ignore_case | ignore | 是否忽略大小写 |
| limit | num, offset | 分页 |
| order_by | field, desc |根据字段进行排序 |

### 5. Where子句操作表达式
| 操作符        | 运算符   |  说明  |
| :--------:   | :-----:  | :----  |
| gt | > | 大于 |
| lt | < | 小于 |
| eq | = | 等于 |
| neq | != | 不等于 |
| egt | >= | 不小于 |
| elt | <= | 不大于 |
| like | LIKE | 字符串模糊查询 |
| in | IN | 集合查询，参数传值为tuple，如: age_in=(28, 29, 30) |
| between | BETWEEN | 介于两值之间，参数传值为两个元素的tuple,如有多个则取第一个和最后一个，如：age_between=(28, 30) |

</font>
