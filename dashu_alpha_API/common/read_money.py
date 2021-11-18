#####根据jobid 读取报价

# from .init_connect import *
# from common.read_mater_name import read_material_name_by_material
from common.init_connect import *
# from init_connect import *

def format_money(row):
    fdata = {}
    cont = 0
    for item in row:
        # print(format_row_money(item)) 
        cont+=1
        fdata[cont]=format_row_money(item)
    return fdata

def format_row_money(item):
    tmp = {}
    tmp['JPID'] = item[0]
    tmp['ID']=item[1]
    tmp['ProductName2']=item[2]
    tmp['ItemName']=item[3].encode('latin-1').decode('gbk')
    tmp['Discount']=float(item[4]) 
    tmp['CateID']=item[5]
    tmp['Category']=item[6].encode('latin-1').decode('gbk')
    tmp['Name']=item[7]
    tmp['Qty']=float(item[8]) 
    print(item[9])
    if item[9]:
        tmp['Price']=float(item[9])
    else:
        tmp['Price'] = 0
    tmp['Length']=float(item[10]) 
    tmp['Width']=float(item[11]) 
    return tmp
    


def read_money_by_JobID(JobID):
    if JobID == '':
        status = False
        msg = "Error step read_money_by_JobID  ,jobID can not empty"
        return status,msg,{}
    try:
        connect = conn()
        if connect:
            # print('数据库链接成功')
            cursor = connect.cursor()
            # print('reading contract_num:',contract_num)
            sql = '''
                select * from (
                select A.JPID,A.ID ID,C.ProductName2,A.PanelName2 ItemName,ISNULL(C.FactoryDiscount,1) Discount,1 CateID,'双饰面板' Category,B.MaterName Name,SUM(A.Length*A.Width*A.Qty/1000000) Qty,A.Price,A.Length Length,A.Width Width                                                                                                           
                from Wrk_JobPanels A left join Bas_Material B on A.Material=B.MaterID
                left join Wrk_JobProducts C on A.JPID=C.JPID
                left join bas_panels e on A.panelID=e.panelID
                where A.JobID=@JobID and  charindex('不报价', isnull(e.description,''))=0                                    
                group by A.JPID,C.ProductName2,A.PanelName2,ISNULL(C.FactoryDiscount,1),A.Material,B.MaterName,A.Price ,A.Length,A.Width,A.Qty,A.ID           
                union all
                select A.JPID,1 ID,C.ProductName2,'异形'  ItemName,1 Discount,2 CateID,'异形' Category,'异形板件' Name,SUM(A.Qty) Qty,10 Price,1 Length,1 Width                                 
                from Wrk_JobPanels A left join Wrk_JobProducts C on A.JPID=C.JPID 
                left join bas_panels e on A.panelID=e.panelID  
                where A.JobID=@JobID and CHARINDEX('异形',A.Memo)>0       and    charindex('异形不算', isnull(e.description,''))=0       
                group by A.JPID,C.ProductName2
                union all    
                select A.JPID,'' ID,C.ProductName2,A.Unit ItemName,1 Discount,2 CateID,'五金' Category,
                    ISNULL(A.WJName2,A.WJName) Name,SUM(case when B.Type=3 then case when isnull(a.unit,'')='根' then A.Qty else ISNULL(A.Length/1000*A.Qty,0)  end else a.qty end) Qty ,   
                    CASE WHEN A.WJName2 IS NOT NULL THEN B.Price ELSE 0 END Price,1 Length,1 Width 
                from Wrk_JobHardware A left join Bas_Hardware B on A.WJID=B.WJID
                left join Wrk_JobProducts C on A.JPID=C.JPID
                where B.PriceType>0 and A.JobID=@JobID  and  charindex('不报价', isnull(b.description,''))=0                                               
                group by A.JPID,C.ProductName2,A.Unit,ISNULL(A.WJName2,A.WJName),
                    CASE WHEN A.WJName2 IS NOT NULL THEN B.Price ELSE 0 END
                union all
                select A.JPID,'' ID,C.ProductName2,'' ItemName,ISNULL(C.FactoryDiscount,1) Discount,3 CateID,'封边材料' Category,
                    A.EdgeName Name,SUM(Length)/1000 Qty,B.Price,1 Length,1 Width                                                  
                from
                (select JPID,EBL1 EdgeName,(Length+20)*Qty Length from Wrk_JobPanels where JobID=@JobID and EBL1<>''
                union all
                select JPID,EBL2 EdgeName,(Length+20)*Qty Length from Wrk_JobPanels where JobID=@JobID and EBL2<>''
                union all
                select JPID,EBW1 EdgeName,(Width+20)*Qty Length from Wrk_JobPanels where JobID=@JobID and EBW1<>''
                union all
                select JPID,EBW2 EdgeName,(Width+20)*Qty Length from Wrk_JobPanels where JobID=@JobID and EBW2<>''
                ) A left join Bas_EdgeBanding B on A.EdgeName=B.EdgeName
                left join Wrk_JobProducts C on A.JPID=C.JPID
                group by A.JPID,C.ProductName2,ISNULL(C.FactoryDiscount,1),A.EdgeName,B.Price   
                union all
                select 999999 JPID,'' ID, A.ProductName2,'' ItemName,ISNULL(B.FactoryDiscount,1) Discount,
                    4 CateID,'组件' Category,A.ProductName2 Name,A.Qty,A.FactoryPrice Price,1 Length,1 Width 
                from Wrk_JobSubs A left join Wrk_JobProducts B on A.JPID=B.JPID where A.JobID=@JobID  and ISNULL(A.FactoryPrice,0)>0                      
                ) A order by JPID,CateID
            '''
            sql = sql.replace('@JobID',JobID)
            # print(sql)
            cursor.execute(sql)
            row = cursor.fetchall()
            cursor.close()   
            connect.close() 
            
            if row == None:
                status = False
                msg = 'No data at read_money'
                data = {}
                return status,msg,{}
            data = format_money(row)
            status = True
            msg = 'read done money'
            return status,msg,data


    except TypeError:
        # print('捕获到类型写入错误 可能数据读混乱了')

        status = False
        msg = "Error step read_money ,The data has been read from the alpha database,but it's empty or format error"
        return status,msg,{}
    except:

        status = False
        msg = "Unable to connect to the alpha server,read_money, please try again later or check the database settings file"
        return status,msg,{}

if __name__ == '__main__':
        data = read_money_by_JobID('4928')
        print('bak:',data)