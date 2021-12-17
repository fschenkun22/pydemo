import pymssql
from configparser import ConfigParser
def conn():
    cfg = ConfigParser()
    cfg.read('./config.ini')
    main_host = cfg.get('alpha','host')
    main_db = cfg.get('database','dbname')
    return pymssql.connect(main_host, 'sa', '123', main_db) #服务器名,账户,密码,数据库名
