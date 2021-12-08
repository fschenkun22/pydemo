import pymssql
from configparser import ConfigParser
def conn():
    cfg = ConfigParser()
    cfg.read('./config.ini')
    main_host = cfg.get('alpha','host')
    return pymssql.connect(main_host, 'sa', '123', 'sjk') #服务器名,账户,密码,数据库名
