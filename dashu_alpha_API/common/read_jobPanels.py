#####根据JPID 找到所有板件 

# from .init_connect import *
from init_connect import *

def format_panels(row):
    tmp = {}
    cont = 0
    ltmp = {}
    for item in row:
        print('bug',type(item),item)
        
        for i in item:
            ltmp['ID'] = item[0]
            cont +=1
        tmp[cont] = ltmp
        cont =0
        ltmp=''
    return tmp

    # tmp = {}
    # cont = 0
    # ltmp = {}
    # for item in row:
    #     for i in item:
    #         ltmp['JPID'] = item[0]
    #         ltmp['width'] = float(item[2]) 
    #         ltmp['height'] = float(item[3]) 
    #         ltmp['panels'] = read_job_panels_by_JPID(str(item[0]))
    #     cont+=1  
    #     tmp[cont] = ltmp
    # cont = 0
    # ltmp = ''
    # return tmp

    return tmp1

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
            msg = 'Success panels read done = '+ JPID
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