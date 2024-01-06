import sqlalchemy 

engine = sqlalchemy.create_engine('mysql://root:123456@localhost:3306/materials', echo=True)

mate_data = sqlalchemy.MetaData()

# person = sqlalchemy.Table(
#     'person', mate_data,
#     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column('name', sqlalchemy.String(50)),
#     sqlalchemy.Column('age', sqlalchemy.Integer),
#     sqlalchemy.Column('address', sqlalchemy.String(100)),
#     sqlalchemy.Column('birthday', sqlalchemy.Date,nullable=False)
# )

# mate_data.create_all(engine)


# 增加一条记录
# person_insert = person.insert().values(name='张三', age=18, address='北京市朝阳区', birthday='2000-01-01')
# with engine.connect() as conn:
#     result = conn.execute(person_insert)
#     conn.commit()
#     print(result.rowcount)

# 插入多条
# person_insert = person.insert().values([
#     {'name': '张三', 'age': 18, 'address': '北京市朝阳区', 'birthday': '2000-01-01'},
#     {'name': '李四', 'age': 19, 'address': '北京市朝阳区', 'birthday': '2001-01-01'},
#     {'name': '王五', 'age': 20, 'address': '北京市朝阳区', 'birthday': '2002-01-01'},
#     {'name': '赵六', 'age': 21, 'address': '北京市朝阳区', 'birthday': '2003-01-01'},
# ])
# with engine.connect() as conn:
#     result = conn.execute(person_insert)
#     conn.commit()
#     print(result.rowcount)



# 查询数据
# person_select = person.select()
# with engine.connect() as conn:
#     result = conn.execute(person_select)
    # 循环所有数据，row[0],row[1] 这样的方式获取数据
    # for row in result:
    #     print(row)

    # 使用fetchone()获取一条数据
    # print(result.fetchone())

    # 使用fetchmany()获取多条数据
    # print(result.fetchmany(2))

    # 使用fetchall()获取所有数据
    # print(result.fetchall())

#   条件查询，查询birthday大于2000-01-01的数据
# person_select = person.select().where(person.c.birthday > '2000-01-01')
# with engine.connect() as conn:
#     result = conn.execute(person_select)
#     print(result.fetchall())

# 更新数据，更新id为1的数据 name 改为大海绵
# person_update = person.update().where(person.c.id == 5).values(name='大海绵')
# with engine.connect() as conn:
#     result = conn.execute(person_update)
#     conn.commit()
#     print(result.rowcount)

# 删除id为5的数据
person_delete = person.delete().where(person.c.id == 5)
with engine.connect() as conn:
    result = conn.execute(person_delete)
    conn.commit()
    print(result.rowcount)