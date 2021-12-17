#####根据jobid 读取报价

from configparser import ConfigParser, Error
from os import error, name

# from .init_connect import *
# from common.read_mater_name import read_material_name_by_material
from common.init_connect import *
# from init_connect import *

cfg = ConfigParser()
cfg.read('./config.ini')

def format_money(row):
    fdata = {}
    cont = 0
    for item in row:
        # print(format_row_money(item)) 
        cont+=1
        fdata[cont]=format_row_money(item)
    return fdata

def format_row_money(item):
    tmp = {}
    # print('准备 try',item)
    JPID =  int(cfg.get('price_col','JPID')) if cfg.get('price_col','JPID') else None
    ID =  int(cfg.get('price_col','ID')) if cfg.get('price_col','ID') else None
    ProductName2 =  int(cfg.get('price_col','ProductName2')) if cfg.get('price_col','ProductName2') else None
    ItemName =  int(cfg.get('price_col','ItemName')) if cfg.get('price_col','ItemName') else None
    Discount =  int(cfg.get('price_col','Discount')) if cfg.get('price_col','Discount') else None
    CateID =  int(cfg.get('price_col','CateID')) if cfg.get('price_col','CateID') else None
    Category =  int(cfg.get('price_col','Category')) if cfg.get('price_col','Category') else None
    Name =  int(cfg.get('price_col','Name')) if cfg.get('price_col','Name') else None
    Qty =  int(cfg.get('price_col','Qty')) if cfg.get('price_col','Qty') else None
    Price =  int(cfg.get('price_col','Price')) if cfg.get('price_col','Price') else None
    Length =  int(cfg.get('price_col','Length')) if cfg.get('price_col','Length') else None
    Width =  int(cfg.get('price_col','Width')) if cfg.get('price_col','Width') else None


    if JPID:
        tmp['JPID']=item[JPID]
    else:
        tmp['JPID'] = '' 
    

    if ID:
        tmp['ID']=item[ID]
    else:
        tmp['ID'] = '' 
    
    if ProductName2:
        tmp['ProductName2']=item[ProductName2]
    else:
        tmp['ProductName2'] = '' 

    if ItemName:
        tmp['ItemName']=item[ItemName].encode('latin-1').decode('gbk')
    else:
        tmp['ItemName'] = '' 
    if Discount:
        tmp['Discount']=float(item[Discount])
    else:
        tmp['Discount'] = '' 

    if CateID:
        tmp['CateID']=item[CateID]
    else:
        tmp['CateID'] = '' 

    if Category:
        tmp['Category']=item[Category].encode('latin-1').decode('gbk')
    else:
        tmp['Category'] = '' 

    if Name:
        tmp['Name']=item[Name]
    else:
        tmp['Name'] = '' 

    if Qty:
        tmp['Qty']=float(item[Qty])
    else:
        tmp['Qty'] = 0 

    if Price:
        tmp['Price']= float(item[Price]) if item[Price] else 0
    else:
        tmp['Price'] = 0 

    if Length:
        tmp['Length']=float(item[Length])
    else:
        tmp['Length'] = 0

    if Width:
        tmp['Width']=float(item[Width])
    else:
        tmp['Width'] = 0 
    # print(123)


        


 

    return tmp
    


def read_money_by_JobID(JobID):
    cfg = ConfigParser()
    cfg.read('./config.ini')
    if JobID == '':
        status = False
        msg = "Error step read_money_by_JobID  ,jobID can not empty"
        return status,msg,{}
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = cfg.get('sql','price')
            sql = sql.replace('@JobID',JobID)
            # print(sql)
            cursor.execute(sql)
            row = cursor.fetchall()
            cursor.close()   
            connect.close() 
            
            if row == None:
                status = False
                msg = 'No data at read_money'
                data = {}
                return status,msg,{}
            print('price result =',row)
            data = format_money(row)
            # data = str(row)
            status = True
            msg = 'read done money'
            return status,msg,data


    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        raise
        status = False
        msg = "Error step read_money ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,{}
    except:

        status = False
        msg = "Unable to connect to the alpha server,read_money, please try again later or check the database settings file"
        return status,msg,{}

if __name__ == '__main__':
        data = read_money_by_JobID('4928')
        print('bak:',data)