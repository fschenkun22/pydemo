#####读合同详情

# from .init_connect import *
from init_connect import *

def format_contract_num(row):
    # print('format data:',row)
    tmp_row = {}
    tmp_row['JobID'] = row[0]
    tmp_row['订单号'] = row[1]
    tmp_row['合同号'] = row[13]
    # print (tmp_row)
    return tmp_row

def read_contract_num_detail(contract_num):
    if contract_num == '':
        status = False
        msg = "Error step read_contract_num_detail,Unable to read contract_num == '' "
        return status,msg,[]
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = "select * from Wrk_Jobs "+"where PactNo="+"'"+contract_num+"'"
            # print(sql)
            # exit()
            cursor.execute(sql)
            row = cursor.fetchone()
            # print(row)
            cursor.close()   
            connect.close()
            status = True
            msg = 'Success contract_num_detail = '+contract_num
            rfrow = format_contract_num(row)
            return status,msg,rfrow
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        status = False
        msg = "Error step read_contract_num ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,[]
    except:
        status = False
        msg = "Unable to connect to the alpha server, please try again later or check the database settings file"
        return status,msg,[]

if __name__ == '__main__':
        data = read_contract_num_detail('20211015-001')
        print('bak:',data)