#####读合同详情

# from .init_connect import *
from init_connect import *
# from init_connect import *

def format_contract_num(row):
    # print('format data:',row)
    tmp_row = {}
    tmp_row['JobID'] = row[0]
    tmp_row['JobNo'] = row[1]
    tmp_row['JobName'] = row[2]
    tmp_row['Client'] = row[3]
    tmp_row['OrderDate'] = row[4].strftime("%Y-%m-%d %H:%M:%S")
    tmp_row['Address'] = row[5]
    tmp_row['LinkMan'] = row[6]
    # tmp_row['DueDate'] = row[7].strftime("%Y-%m-%d %H:%M:%S")
    tmp_row['Memo'] = row[8]
    tmp_row['Tel'] = row[12]
    tmp_row['IsLock'] = row[14]
    tmp_row['State'] = row[19]
    tmp_row['Area'] = float(row[29]) 
    tmp_row['Barcode'] = row[34]




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
            # print('row is',row)
            cursor.close()   
            connect.close()
            if row == None:
                status = False
                msg = 'No Data'
                data = {}
                return status,msg,data
            status = True
            msg = 'Success contract_num_detail = '+contract_num
            rfrow = format_contract_num(row)
            return status,msg,rfrow
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        # raise
        status = False
        msg = "Error step read_contract_num ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,[]
    except:
        status = False
        msg = "Unable to connect to the alpha server, please try again later or check the database settings file"
        return status,msg,[]

if __name__ == '__main__':
        data = read_contract_num_detail('211119-001-1')
        print('bak:',data)