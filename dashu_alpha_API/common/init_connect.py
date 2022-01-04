import pymssql
from configparser import ConfigParser
def conn():
    cfg = ConfigParser()
    cfg.read('./config.ini')
    main_host = cfg.get('alpha','host')
    main_db = cfg.get('database','dbname')
    return pymssql.connect(str(main_host), 'sa', '123', str(main_db))
