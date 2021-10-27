from types import NoneType
import pymssql


def format_data(row):
    # print('format data:',row)
    tmp_row = {}
    tmp_row['alpha_id'] = row[0]
    tmp_row['订单号'] = row[1]
    tmp_row['合同号'] = row[13]

    print (tmp_row)
    return tmp_row



def read_contract_num(contract_num):
    try:
        connect = pymssql.connect('192.168.1.151\SQLEXPRESS', 'sa', '123', 'sjk') #服务器名,账户,密码,数据库名
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
            msg = 'success to connect alpha database!'
            rfrow = format_data(row)
            return status,msg,rfrow
            
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        status = False
        msg = "The data has been read from the alpha database,but it's empty or format error"
        return status,msg,None
    except:
        status = False
        msg = "Unable to connect to the alpha server, please try again later or check the database settings file"
        return status,msg,None


if __name__ == '__main__':
   data = read_contract_num('20211015-0013333')
   print('main print data:',data)