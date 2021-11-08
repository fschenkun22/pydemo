
######读合同下有多少个柜子
####@param JobID 4928

# JobID 是通过合同号查出来的唯一ID
# 查询结果是所有产品（也就是有多少柜）
import copy
from common.read_hardware import *
from common.init_connect import *
from common.read_jobPanels import *

def read_job_products_list_by_JobID(JobID):
    #### 通过jobID 查询jobProducts中有几个柜子，并列出柜子大小 4928
    # print('收到jobid:',JobID)
    try:
        connect = conn()
        if connect:
            cursor = connect.cursor()
            sql = "select JPID,ProductName2,Width,Depth,Height,Memo from Wrk_JobProducts "+"where JobID="+"'"+JobID+"'"
            cursor.execute(sql)
            row = cursor.fetchall()
            cursor.close()   
            connect.close()

            status = True
            msg = 'read contract board list done'

            # print(row)
            # exit()
            data = format_row(row)


            return status,msg,data

    except TypeError:
    # print('捕获到类型写入错误 可能数据读混乱了')
        status = True
        msg = "This maybe not an error! step read_contract_board_list ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,[]
    except:
        status = False
        msg = "Unable to connect to the alpha server, please try again later or check the database settings file"
        return status,msg,[]

def format_row(row):
    print('debug1',row)
    tmp = {}
    cont = 0
    ltmp = {}
    panlestmp = {}
    for item in row:
        print('jpid',item[0])
        ltmp['JPID'] = item[0]
        ltmp['ProductName2']=item[1]
        ltmp['Width'] = float(item[2]) 
        ltmp['Depth'] = float(item[3]) 
        ltmp['Height'] = float(item[4]) 
        ltmp['Memo'] = item[5]
            # 从这开始利用JPID搜索组件当中各种数据，第一个数据为panel，第二个为五金，!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 在这里增加读取种类 ，如门板 生产数据等
            # ########################所有工件###################

        data = read_job_panels_by_JPID(str(item[0])) ##

            # print('bug data is ',data)
        ltmp['panels']=data[2]
            # data = []
            # ###################################################

            # ########################所有五金件##################

        data = read_job_hardware_by_JPID(str(item[0]))

        ltmp['hardwares']=data[2]



        #######################################################################################################################################################
        cont+=1
        tmp[cont] = ltmp.copy()



    cont = 0
    ltmp = ''

    return tmp


if __name__ == '__main__':
    data = read_job_products_list_by_JobID('4928')
    print(data)
    