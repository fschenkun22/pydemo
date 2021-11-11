from urllib.parse import quote,unquote,urlparse,parse_qs

def format_contract_str(contract_str):

    data={} ## 定义返回的数组
    data['status']=False
    data['msg']=''
    data['data']={}

    try:
        tmpdata = unquote(contract_str)
        up = urlparse(tmpdata)
        upp = parse_qs(up.query)
        # names = ['PactNo','JobNo','JobName','Client','OrderDate','Address','LinkMan','Memo','Tel','GUID','Designer','Calculator','Dealer']
        print('unpack data:',upp)

        #######检查#######
        if len(upp['PactNo'][0])<50:
            print('yes',len(upp['PactNo'][0]))
        else:
            data['status'] = False
            data['msg']='PactNo error'
            return data

    except:
        raise





def write_contract_by(contract_str):

    ## 把传过来的参数格式化并检测有问题没，有问题返回错误，没问题继续
    # job = format_contract_str(contract_str)
    return format_contract_str(contract_str) 


    pass


if __name__ == '__main__':
        data = write_contract_by('/?PactNo=%E5%90%88%E5%90%8C%E5%8F%B7%E6%B5%8B%E8%AF%95&JobNo=20211110%E5%8D%95%E5%8F%B7%E6%B5%8B%E8%AF%95&JobName=%E8%AE%A2%E5%8D%95%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&Client=%E5%AE%A2%E6%88%B7%E5%90%8D%E7%A7%B0%E6%B5%8B%E8%AF%95&OrderDate=now&Address=%E5%AE%89%E8%A3%85%E5%9C%B0%E5%9D%80%E6%B5%8B%E8%AF%95&LinkMan=%E8%81%94%E7%B3%BB%E4%BA%BA%E6%B5%8B%E8%AF%95&Memo=%E5%A4%87%E6%B3%A8%E6%B5%8B%E8%AF%95&Tel=15641366461&GUID=random&Designer=%E8%AE%BE%E8%AE%A1%E5%B8%88%E6%B5%8B%E8%AF%95&Calculator=%E6%8B%86%E5%8D%951&Dealer=%E4%BB%A3%E7%90%86%E5%95%86%E5%90%8D%E6%B5%8B%E8%AF%95')
        print('maindata is',data)