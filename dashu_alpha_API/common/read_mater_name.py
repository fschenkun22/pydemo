## 根据materialID 读取mater name

# from .init_connect import *
from common.init_connect import *

def format_mater(row):
    tmp = {}
    tmp['MaterID'] = row[0][0]
    tmp['MaterName']=row[0][1]
    tmp['Color']=row[0][2]
    tmp['Thickness']=float(row[0][3])
    tmp['Material']=row[0][4]

    return tmp



def read_material_name_by_material(material):
    if material == '':
        status = False
        msg = "Error step read_jobhardware,Unable to read JPID == '' "
        return status,msg,{}
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = "select MaterID,MaterName,Color,Thickness,Material from Bas_Material "+"where MaterID="+"'"+material+"'"
            # print(sql)
            # exit()
            cursor.execute(sql)
            row = cursor.fetchall()
            # print(row)
            cursor.close()   
            connect.close()
            status = True
            msg = 'Success materID read done materID is = '+ material
            data = format_mater(row)
            # print('bug data type is ',data)
            return data
    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')
        status = False
        msg = "Error step read_matername ,The data has been read from the alpha database,but it's empty or format error"
        return {}
    except:
        status = False
        msg = "Unable to connect to the alpha server,read_hardware, please try again later or check the database settings file"
        return {}

if __name__ == '__main__':
        data = read_material_name_by_material('6672')
        print('bak:',data)