## 读取所有合同数据

## 第一步读合同号信息
import common.read_jobProducts_list
import common.read_contract_num_detail


def get_full(contract_num):
    ##  读合同号内容
    status = False
    msg = 'read_contract_num_detail => get_full defalt out put'
    data = {}
    ## 调用读取函数
    contract_detail = common.read_contract_num_detail.read_contract_num_detail(contract_num)
    if contract_detail[0] == True:
        ## 成功获取合同信息
        status = contract_detail[0]
        msg = contract_detail[1]
        data['header_detail'] = contract_detail[2]
        ## 拿JobID去找，有多少个part 直接读part数据存
        JobID = str(data['header_detail']['JobID'])
        print('JobID = ',JobID) 
        ## 拿JobID去找JobProducts
        JobList = common.read_jobProducts_list.read_job_products_list_by_JobID(JobID)
        print('jobid 查询的结果',JobList)
        ## 判断结果如果为假说明错误了，把错误信息返回，如果正确继续
        if JobList[0] == True:
            ## 到这 说明拿到结果对了
            # data['part'] = JobList[2] ##所有部件存在part里
            # print('结果正确下一步根据数据列表循返回出数据 看下jobList内容：',JobList[2])
            data['parts'] = JobList[2]
            
        else:
            status = False
            msg = JobList[1]
            data = {}
        return status,msg,data

    ## 读取合同失败处理    
    else:
        status = contract_detail[0]
        msg = contract_detail[1]
        return status,msg,{}
    


if __name__ == "__main__":
   data = get_full('20211015-003')
   print('main data = ',data)