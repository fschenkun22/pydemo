import sqlalchemy
from sqlalchemy import text,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine('mysql://root:123456@localhost:3306/test_materials', echo=True)

# Working with Transactions and the DBAPI¶ 直接用text方式的读取
# with engine.connect() as conn:
#     result = conn.execute(text("select * from employee"))
#     print(result.fetchall())

    # 增加添加数据
    # conn.execute(
    #     text("insert into employee (ename,name) values(:x,:y)"),
    #     [{"x": "小明", "y": "xiaoming"}, {"x": "小红", "y": "xiaohong"}],
    #     )
    # conn.commit()

    # 结果使用mappings()方法 把数据库获取的对象直接变成对象格式
    # result = conn.execute(text("select * from employee where emp_id > 30"))
    # for row in result.mappings():
    #     print(row['emp_id'])

# 用session模式读取
# stmt = text("select * from employee where emp_id > :x")
# with Session(engine) as session:
#     result = session.execute(stmt, {"x": 30})
#     for row in result.mappings():
#         print(row['emp_id'])
#     session.commit()

# 用session模式写入
# stmt = text("insert into employee (ename,name) values(:x,:y)")
# with Session(engine) as session:
    # session.execute(stmt, [{"x": "小明", "y": "xiaoming"}, {"x": "小红", "y": "xiaohong"}])
    # session.commit()

    # 更新 ename为小红的数据, 注意y里存储的是要修改标记的行, x里存储的是修改的值
    # stmt = text("update employee set name = :x where ename = :y")
    # session.execute(stmt, {"x": "修改的值", "y": "小红"})
    # session.commit()

    # 删除ename为小红的数据
    # stmt = text("delete from employee where ename = :x")
    # session.execute(stmt, {"x": "小红"})
    # session.commit()

#  使用metadata方式读取

metadata_obj = MetaData()

employee_table = Table(
    "employee",
    # 自动加载数据
    metadata_obj,
    Column("emp_id", Integer, primary_key=True),
    Column("ename", String(50)),
    Column("emp_station_num", String(50)),
)

# 读取数据 获取employee_table所有数据
with engine.connect() as conn:
    result = conn.execute(employee_table.select())
    for row in result.mappings():
        print(row)


