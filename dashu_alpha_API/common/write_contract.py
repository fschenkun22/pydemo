#### 接单写入
from datetime import datetime
from urllib.parse import quote,unquote,urlparse,parse_qs
import re
import datetime
import uuid

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
            print('debug JobNo is',len(upp['JobNo'][0]))
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
        print('debug OrderDate is ',upp['OrderDate'][0])
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

        data['data'] = collect_data ## 写入要返回数据
        data['status'] = True
        data['msg'] = 'success ,All checked pass'
        return data


    except:
        raise
    ## here are some unkown errors





def write_contract_by(contract_str):

    ## 把传过来的参数格式化并检测有问题没，有问题返回错误，没问题继续
    # job = format_contract_str(contract_str)
    return format_contract_str(contract_str) 


    pass


if __name__ == '__main__':
        data = write_contract_by('/?PactNo=211112-001-1-1&JobNo=20211110%E5%8D%95%E5%8F%B7%E6%B5%8B%E8%AF%95&JobName=%E8%AE%A2%E5%8D%95%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&Client=%E5%AE%A2%E6%88%B7%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&OrderDate=now&Address=%E5%AE%89%E8%A3%85%E5%9C%B0%E5%9D%80%E6%B5%8B%E8%AF%95&LinkMan=%E8%81%94%E7%B3%BB%E4%BA%BA%E6%B5%8B%E8%AF%95&Memo=%E5%A4%87%E6%B3%A8%E6%B5%8B%E8%AF%95&Tel=15641366461&GUID=random&Designer=%E8%AE%BE%E8%AE%A1%E5%B8%88%E6%B5%8B%E8%AF%95&Calculator=%E6%8B%86%E5%8D%951&Dealer=%E4%BB%A3%E7%90%86%E5%95%86%E5%90%8D%E6%B5%8B%E8%AF%95')
        print('maindata is',data)