## 根据materialID 读取mater name

# from .init_connect import *
from common.init_connect import *
# from init_connect import *

def format_mater(row):
    tmp = {}
    tmp['PanelType'] = row[0][0]

    return tmp



def read_material_paneltype_by_PanelID(PanelID):
    if PanelID == '':
        status = False
        msg = "Error step read_jobhardware,Unable to read JPID == '' "
        return status,msg,{}
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = "select PanelType from Bas_Panels "+"where PanelID="+"'"+PanelID+"'"
            # print(sql)
            # exit()
            cursor.execute(sql)
            row = cursor.fetchall()
            # print(row)
            cursor.close()   
            connect.close()
            status = True
            msg = 'Success materID read done materID is = '+ PanelID
            data = format_mater(row)
            # print('bug data type is ',data)
            return data
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        # raise
        status = False
        msg = "Error step read_matername ,The data has been read from the alpha database,but it's empty or format error"
        return {}
    except:
        # raise
        status = False
        msg = "Unable to connect to the alpha server,read_hardware, please try again later or check the database settings file"
        return {}

if __name__ == '__main__':
        data = read_material_paneltype_by_PanelID('1192')
        print('bak:',data)