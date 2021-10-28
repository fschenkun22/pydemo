import pymssql


def format_contract_num(row):
    # print('format data:',row)
    tmp_row = {}
    tmp_row['alpha_id'] = row[0]
    tmp_row['订单号'] = row[1]
    tmp_row['合同号'] = row[13]
    print (tmp_row)
    return tmp_row

def conn():
    return pymssql.connect('192.168.1.151\SQLEXPRESS', 'sa', '123', 'sjk') #服务器名,账户,密码,数据库名

def read_contract_all(contract_num):
    status = ''
    msg = ''
    result = {}
    res = read_contract_num(contract_num)
    status = res[0]
    msg = res[1]
    result['contract_header_detail'] = res[2]
    ##现在应该获取到JobID，唯一
    JobID = str(res[2]['alpha_id'])
    print('jobID is',JobID,type(JobID))
    data = read_contract_board_list(JobID)
    print(data)

    ##下一步开始循环读出来所有product
    if status == False:
        return status,msg,[]



    return status,msg,result

def read_contract_num(contract_num):
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
            msg = 'success to connect alpha database!'
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

def read_contract_board_list(JobID):
    #### 通过jobID 查询jobProducts中有几个柜子，并列出柜子大小
    try:
        connect = conn()
        if connect:
            cursor = connect.cursor()
            sql = "select JPID,ProductName2,Width,Depth,Height,ProductIndex from Wrk_JobProducts "+"where JobID="+"'"+JobID+"'"
            cursor.execute(sql)
            row = cursor.fetchall()
            cursor.close()   
            connect.close()


            status = True
            msg = 'read contract board list done'
            return status,msg,row

    except TypeError:
    # print('捕获到类型写入错误 可能数据读混乱了')
        raise
        status = True
        msg = "This maybe not an error! step read_contract_board_list ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,[]
    except:
        raise
        status = False
        msg = "Unable to connect to the alpha server, please try again later or check the database settings file"
        return status,msg,[]

def read_contract_door_list():
    pass

def read_contract_hardware_list():
    pass


if __name__ == '__main__':
#    data = read_contract_num('20211015-0013333')
#    print('main print data:',data)
  data = read_contract_all("20211015-003")
  # data = read_contract_board_list('4928')
  print(data)