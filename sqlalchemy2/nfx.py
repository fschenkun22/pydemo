
import sqlalchemy #注意现在使用的版本是2.0,所有语法参考官方2.0文档https://docs.sqlalchemy.org/en/20/dialects/mysql.html

engine = sqlalchemy.create_engine('mysql://root:123456@localhost:3306/test_materials', echo=True)

meta_data = sqlalchemy.MetaData(schema='test_materials')

