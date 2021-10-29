import pymssql

def conn():
    return pymssql.connect('192.168.1.151\SQLEXPRESS', 'sa', '123', 'sjk') #服务器名,账户,密码,数据库名