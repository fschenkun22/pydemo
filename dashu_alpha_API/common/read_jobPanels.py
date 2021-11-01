#####根据JPID 找到所有板件 

# from .init_connect import *
from init_connect import *

def format_panels(row):
    tmp = {}
    cont = 0
    ltmp = {}

    for item in row:
       
        # print(cont,'返回的id数据',item[0])
        tmp[cont] = get_by_JPID(item[0],row,cont)
        cont+=1
   
    return tmp

def get_by_JPID(JPID,row,cont):
    tmp={}
    # print('bug...',row[cont])
    # print('bug2...',row[cont][0])
    # print('bug3...',row[cont][1])
    # print('bug4...',row[cont][2])
    tmp['id'] = row[cont][0]
    tmp['JPID'] = row[cont][1]
    tmp['PanleName2']=row[cont][2].encode('latin-1').decode('gbk')
    return tmp



def read_job_panels_by_JPID(JPID):
    if JPID == '':
        status = False
        msg = "Error step read_jobPanels,Unable to read JPID == '' "
        return status,msg,[]
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = "select ID,JPID,PanelName2 from Wrk_JobPanels "+"where JPID="+"'"+JPID+"'"
            # print(sql)
            # exit()
            cursor.execute(sql)
            row = cursor.fetchall()
            # print(row)
            cursor.close()   
            connect.close()
            status = True
            msg = 'Success panels read done JPID is = '+ JPID
            data = format_panels(row)
            return status,msg,data
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        raise
        status = False
        msg = "Error step read_jobPanels ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,[]
    except:
        raise
        status = False
        msg = "Unable to connect to the alpha server,read_jobPanels, please try again later or check the database settings file"
        return status,msg,[]

if __name__ == '__main__':
        data = read_job_panels_by_JPID('24305')
        print('bak:',data)