#### 接单写入
from datetime import datetime
from urllib.parse import quote,unquote,urlparse,parse_qs
import re
import datetime
import uuid
import time
from common.init_connect import *
from common.read_contract_num_detail import *

## 翻译接单数据
def format_contract_str(contract_str):
    data={} ## 定义返回的数组
    data['status']=False
    data['msg']=''
    data['data']={}
    collect_data = {}
    print('debug:',contract_str)
    try:

        tmpdata = urlparse(contract_str) # 解码
        print('tmpdata:',tmpdata)
        # up = unquote(tmpdata.query) 
        # 
        up = tmpdata.query
        print('up:',up)
        upp = parse_qs(up)

        
        print('upp:',upp)
        # names = ['PactNo','JobNo','JobName','Client','OrderDate','Address','LinkMan','Memo','Tel','GUID','Designer','Calculator','Dealer']
        # print('unpack data:',upp)
        # print('debug pactNo is ',upp['PactNo'][0])
        #######检查#######PactNo
        if re.match(r'^\d{6}-\d{3,4}|^B{1}\d{6}-\d{3,4}',upp['PactNo'][0]):
            print('checked PackNo success',upp['PactNo'][0])
            collect_data['PactNo']=upp['PactNo'][0]
        else:
            ## 失败中断返回错误内容
            data['status'] = False
            data['msg']='PactNo format error,format must be "^\d{6}-\d{3,4}|^B{1}\d{6}-\d{3,4}"'
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
            collect_data['OrderDate'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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
        raise
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
    # print('ref_data is :',ref_data)
    if ref_data['status'] == True:
        # print('format checked pass:',ref_data['data']['PactNo'])
        ## 能到达这说明基本格式没有问题，拿合同号去查合同号是否存在
        pre_data = ref_data['data']
        contract_num = read_contract_num_detail(ref_data['data']['PactNo'])
        # print('查询合同号结果:',contract_num)
        if contract_num[0] == False:
            # print('没有检测到该合同任何数据，可以下单了')
            try:
                connect = conn()
                if connect:
                    cursor = connect.cursor()

                    # print('ref：', ref_data)
                    sql='insert into Wrk_Jobs(JobNo,JobName,Client,OrderDate,Address,LinkMan,Memo,Tel,PactNo,IsLock,State,GUID,Designer,Calculator,Dealer)values('+"'"+pre_data['JobNo']+"'"+','+"'"+pre_data['JobName']+"'"+','+"'"+pre_data['Client']+"'"+','+"'"+pre_data['OrderDate']+"'"+','+"'"+pre_data['Address']+"'"+','+"'"+pre_data['LinkMan']+"'"+','+"'"+pre_data['Memo']+"'"+','+"'"+pre_data['Tel']+"'"+','+"'"+pre_data['PactNo']+"'"+','+'0'+','+'0'+','+"'"+pre_data['GUID']+"'"+','+"'"+pre_data['Designer']+"'"+','+"'"+pre_data['Calculator']+"'"+','+"'"+pre_data['Dealer']+"'"+')'
                    
                    # print('sql is',sql)
                    
                    cursor.execute(sql)
                    ## 应该判断写入位是否为55aa ，如果是 写入，写入错误返回错误
                    if pre_data['Write_enable'] == '55aa':
                        connect.commit()
                    cursor.close()
                    connect.close()

                    data['status'] = True
                    data['msg'] = 'write done'
                    return data
            except:
                    data['status'] = False
                    data['msg'] = 'Write contract error, connect database error'
                    return data




        else:
            # print('不能下单 ，找到一个相同合同号的信息：',contract_num[2])
            data['status'] = False
            data['msg']='this contract has allrady exsist ,',contract_num[2]
            return data



    else:
        # print('不通过直接报错')
        data['status'] = False
        data['msg'] = 'checked format error, write failed,'+ref_data['msg']
        return data




if __name__ == '__main__':
        data = write_contract_by('/?PactNo=111122-001-1&JobNo=20211110%E5%8D%95%E5%8F%B7%E6%B5%8B%E8%AF%95&JobName=%E8%AE%A2%E5%8D%95%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&Client=%E5%AE%A2%E6%88%B7%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&OrderDate=now&Address=%E5%AE%89%E8%A3%85%E5%9C%B0%E5%9D%80%E6%B5%8B%E8%AF%95&LinkMan=%E8%81%94%E7%B3%BB%E4%BA%BA%E6%B5%8B%E8%AF%95&Memo=%E5%A4%87%E6%B3%A8%E6%B5%8B%E8%AF%95&Tel=15641366461&GUID=random&Designer=%E8%AE%BE%E8%AE%A1%E5%B8%88%E6%B5%8B%E8%AF%95&Calculator=%E6%8B%86%E5%8D%951&Dealer=%E4%BB%A3%E7%90%86%E5%95%86%E5%90%8D%E6%B5%8B%E8%AF%95&Write_enable=test')
        print('maindata is',data)