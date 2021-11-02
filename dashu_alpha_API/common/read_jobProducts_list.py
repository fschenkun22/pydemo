
######读合同下有多少个柜子
####@param JobID 4928

# JobID 是通过合同号查出来的唯一ID
# 查询结果是所有产品（也就是有多少柜）
from init_connect import *
from read_jobPanels import *

def read_job_products_list_by_JobID(JobID):
    #### 通过jobID 查询jobProducts中有几个柜子，并列出柜子大小 4928
    # print('收到jobid:',JobID)
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
            data = format_row(row)
            return status,msg,data

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

def format_row(row):
    tmp = {}
    cont = 0
    ltmp = {}
    panlestmp = {}
    for item in row:
        for i in item:
            ltmp['JPID'] = item[0]
            ltmp['width'] = float(item[2]) 
            ltmp['height'] = float(item[3]) 
            data = read_job_panels_by_JPID(str(item[0])) ### bug 不知道为啥变成数组了
            print('bug data is ',data)
            panlestmp['status'] = data[0]
            panlestmp['msg']=data[1]
            panlestmp['data']=data[2]
            ltmp['panels']=panlestmp

        cont+=1  
        tmp[cont] = ltmp
    cont = 0
    ltmp = ''
    return tmp


if __name__ == '__main__':
    data = read_job_products_list_by_JobID('4928')
    print(data)
    