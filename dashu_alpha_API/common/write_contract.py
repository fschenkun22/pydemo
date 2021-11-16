#### 接单写入
from datetime import datetime
from urllib.parse import quote,unquote,urlparse,parse_qs
import re
import datetime
import uuid

from common.init_connect import *
import pprint

## 翻译接单数据
def format_contract_str(contract_str):
    data={} ## 定义返回的数组
    data['status']=False
    data['msg']=''
    data['data']={}
    collect_data = {}

    try:
        tmpdata = unquote(contract_str)
        up = urlparse(tmpdata)
        upp = parse_qs(up.query)
        # names = ['PactNo','JobNo','JobName','Client','OrderDate','Address','LinkMan','Memo','Tel','GUID','Designer','Calculator','Dealer']
        print('unpack data:',upp)   
        # print('debug pactNo is ',upp['PactNo'][0])
        #######检查#######PactNo
        if re.match(r'^\d{6}-\d{3,4}|^B{1}\d{6}-\d{3,4}',upp['PactNo'][0]):
            print('checked PackNo success',upp['PactNo'][0])
            collect_data['PactNo']=upp['PactNo'][0]
        else:
            ## 失败中断返回错误内容
            data['status'] = False
            data['msg']='PactNo not found'
            data['data']={}
            return data
        ##################

        #######检查#######JobNo
        if len(upp['JobNo'][0])<256:
            # print('debug JobNo len is',len(upp['JobNo'][0]))
            collect_data['JobNo']=upp['JobNo'][0]
        else:
            data['status']=False
            data['msg']='JobNo limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######JobName
        if len(upp['JobName'][0])<256:
            collect_data['JobName']=upp['JobName'][0]
        else:
            data['status']=False
            data['msg']='JobName limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######Client
        if len(upp['Client'][0])<256:
            collect_data['Client']=upp['Client'][0]
        else:
            data['status']=False
            data['msg']='Client limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######OrderDate
        # print('debug OrderDate is ',upp['OrderDate'][0])
        if upp['OrderDate'][0] =='now':
            collect_data['OrderDate'] = datetime.datetime.now()
        else:
            data['status']=False
            data['msg']='OrderDate must be now'
            data['data']={}
            return data
        ##################

        #######检查#######Address
        if len(upp['Address'][0])<256:
            collect_data['Address']=upp['Address'][0]
        else:
            data['status']=False
            data['msg']='Address limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######LinkMan
        if len(upp['LinkMan'][0])<256:
            collect_data['LinkMan']=upp['LinkMan'][0]
        else:
            data['status']=False
            data['msg']='LinkMan limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查######Memo
        if len(upp['Memo'][0])<256:
            collect_data['Memo']=upp['Memo'][0]
        else:
            data['status']=False
            data['msg']='Memo limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查######Tel
        if len(upp['Tel'][0])<256:
            collect_data['Tel']=upp['Tel'][0]
        else:
            data['status']=False
            data['msg']='Tel limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查######GUID
        if upp['GUID'][0] == 'random':
            collect_data['GUID'] = str(uuid.uuid4())
        else:
            data['status']=False
            data['msg']='GUID must be random'
            data['data']={}
            return data
        ##################

        #######检查######Designer
        if len(upp['Designer'][0])<256:
            collect_data['Designer']=upp['Designer'][0]
        else:
            data['status']=False
            data['msg']='Designer limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######Calculator
        if len(upp['Calculator'][0])<256:
            collect_data['Calculator']=upp['Calculator'][0]
        else:
            data['status']=False
            data['msg']='Calculator limited in range 255'
            data['data']={}
            return data
        ###################

        #######检查#######Dealer
        if len(upp['Dealer'][0])<256:
            collect_data['Dealer']=upp['Dealer'][0]
        else:
            data['status']=False
            data['msg']='Dealer limited in range 255'
            data['data']={}
            return data
        ##################

        #######检查#######Write_enable ##除传入55aa外 所有信号都忽略不写入
        if len(upp['Write_enable'][0])<10:
            collect_data['Write_enable']=upp['Write_enable'][0]
        else:
            data['status']=False
            data['msg']='Write_enable limited in range 10'
            data['data']={}
            return data
        ##################


        data['data'] = collect_data ## 写入要返回数据
        data['status'] = True
        data['msg'] = 'success ,All checked pass'
        return data


    except:
        data['data']=''
        data['status']=False
        data['msg']='error when format contract str'
        return data
    ## here are some unkown errors


def write_contract_by(contract_str):

    data={}

    ## 把传过来的参数格式化并检测有问题没，有问题返回错误，没问题继续

    ref_data = format_contract_str(contract_str)
    ### 格式化数据后开始正式写入
    if ref_data['status'] == True:
        print('通过检测',ref_data['data'])
        try:
            connect = conn()
            if connect:
                cursor = connect.cursor()
                sql='''select * from (
select A.JPID,A.ID ID,C.ProductName2,A.PanelName2 ItemName,ISNULL(C.FactoryDiscount,1) Discount,1 CateID,'双饰面板' Category,B.MaterName Name,SUM(A.Length*A.Width*A.Qty/1000000) Qty,A.Price,A.Length Length,A.Width Width                                                                                                           
from Wrk_JobPanels A left join Bas_Material B on A.Material=B.MaterID
  left join Wrk_JobProducts C on A.JPID=C.JPID
   left join bas_panels e on A.panelID=e.panelID
where A.JobID=4928 and  charindex('不报价', isnull(e.description,''))=0                                    
group by A.JPID,C.ProductName2,A.PanelName2,ISNULL(C.FactoryDiscount,1),A.Material,B.MaterName,A.Price ,A.Length,A.Width,A.Qty,A.ID           
union all
select A.JPID,1 ID,C.ProductName2,'异形'  ItemName,1 Discount,2 CateID,'异形' Category,'异形板件' Name,SUM(A.Qty) Qty,10 Price,1 Length,1 Width                                 
from Wrk_JobPanels A left join Wrk_JobProducts C on A.JPID=C.JPID 
   left join bas_panels e on A.panelID=e.panelID  
where A.JobID=4928 and CHARINDEX('异形',A.Memo)>0       and    charindex('异形不算', isnull(e.description,''))=0       
group by A.JPID,C.ProductName2
union all    
select A.JPID,'' ID,C.ProductName2,A.Unit ItemName,1 Discount,2 CateID,'五金' Category,
	ISNULL(A.WJName2,A.WJName) Name,SUM(case when B.Type=3 then case when isnull(a.unit,'')='根' then A.Qty else ISNULL(A.Length/1000*A.Qty,0)  end else a.qty end) Qty ,   
	CASE WHEN A.WJName2 IS NOT NULL THEN B.Price ELSE 0 END Price,1 Length,1 Width 
from Wrk_JobHardware A left join Bas_Hardware B on A.WJID=B.WJID
  left join Wrk_JobProducts C on A.JPID=C.JPID
where B.PriceType>0 and A.JobID=4928  and  charindex('不报价', isnull(b.description,''))=0                                               
group by A.JPID,C.ProductName2,A.Unit,ISNULL(A.WJName2,A.WJName),
	CASE WHEN A.WJName2 IS NOT NULL THEN B.Price ELSE 0 END
union all
select A.JPID,'' ID,C.ProductName2,'' ItemName,ISNULL(C.FactoryDiscount,1) Discount,3 CateID,'封边材料' Category,
	A.EdgeName Name,SUM(Length)/1000 Qty,B.Price,1 Length,1 Width                                                  
from
(select JPID,EBL1 EdgeName,(Length+20)*Qty Length from Wrk_JobPanels where JobID=4928 and EBL1<>''
union all
select JPID,EBL2 EdgeName,(Length+20)*Qty Length from Wrk_JobPanels where JobID=4928 and EBL2<>''
union all
select JPID,EBW1 EdgeName,(Width+20)*Qty Length from Wrk_JobPanels where JobID=4928 and EBW1<>''
union all
select JPID,EBW2 EdgeName,(Width+20)*Qty Length from Wrk_JobPanels where JobID=4928 and EBW2<>''
) A left join Bas_EdgeBanding B on A.EdgeName=B.EdgeName
  left join Wrk_JobProducts C on A.JPID=C.JPID
group by A.JPID,C.ProductName2,ISNULL(C.FactoryDiscount,1),A.EdgeName,B.Price   
                     
) A order by JPID,CateID'''
                cursor.execute(sql)

                index = cursor.description
                tem1 = cursor.fetchone()
                print('debug:!11:',tem1)
                print('debug:!22:',index)

                # print('debug ref_data is :',ref_data['data'])
                # print('sql is',sql)
                cursor.close()
                connect.close()

                data['status'] = True
                data['msg'] = 'write done'
                return data
        except:
                data['status'] = False
                data['msg'] = 'connect database error'
                return data

    else:
        print('不通过')
        data['status'] = False
        data['msg'] = 'checked format error, write failed'
        return data




if __name__ == '__main__':
        data = write_contract_by('/?PactNo=B211115-001WB-1-1&JobNo=20211110%E5%8D%95%E5%8F%B7%E6%B5%8B%E8%AF%95&JobName=%E8%AE%A2%E5%8D%95%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&Client=%E5%AE%A2%E6%88%B7%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&OrderDate=now&Address=%E5%AE%89%E8%A3%85%E5%9C%B0%E5%9D%80%E6%B5%8B%E8%AF%95&LinkMan=%E8%81%94%E7%B3%BB%E4%BA%BA%E6%B5%8B%E8%AF%95&Memo=%E5%A4%87%E6%B3%A8%E6%B5%8B%E8%AF%95&Tel=15641366461&GUID=random&Designer=%E8%AE%BE%E8%AE%A1%E5%B8%88%E6%B5%8B%E8%AF%95&Calculator=%E6%8B%86%E5%8D%951&Dealer=%E4%BB%A3%E7%90%86%E5%95%86%E5%90%8D%E6%B5%8B%E8%AF%95&Write_enable=test')
        print('maindata is',data)