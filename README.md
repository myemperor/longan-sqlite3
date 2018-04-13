<font style='font-family:Courier New '>

# 欢迎使用longan-sqlite3 v0.3

------

我们理解您需要更便捷更高效更轻量级的工具记录数据，并将其中承载的价值传播给他人，**longan-sqlite3** 是我们给出的答案 ———— 让您随心所欲的完成如下功能

> * Create
> * Research
> * Update
> * Delete

![longan-sqlite3-logo](https://img-blog.csdn.net/20180329103235613)



> 您现在看到的这个 longan-sqlite3 版本，仅为开发版，功能将陆续增加

> 0.3 新增分组聚合函数

> 0.2 修复了主键判断，修复了handler接口
------

## 什么是 longan

longan 是一种水果，就是他很甜，喜欢的人吃很多，不喜欢的人一吃就上火

### 1. 以下是我们计划中的功能 

- [x] 支持 CRUD
- [x] 支持 分组聚合函数
- [ ] 新增 where 语句支持
- [ ] 修复 代码注释

### 2. 以下是我们的行为守恒公式

$$longan=mc^2$$

### 3. 使用方法

 - 导入longan
```python
from longan_sqlite import Longan, Flesh
```
 - 实例化longan
```python
longan = Longan('test.db', 'company')
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
 - 通过如下方式创建
```python
longan.execute_file('company.sql')
```


### 4. API文档

| 接口        | 参数   |  说明  |
| --------   | -----:  | :----:  |
| -          | - |   -     |

</font>
