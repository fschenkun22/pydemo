
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# from common_fn import read_contract_num_detail as readContractNumDetail


sys.path.append("./common/")
from common.read_full_contract_num import get_full
data = {'code':'200'}
host = ('0.0.0.0', 8888)
 
class Resquest(BaseHTTPRequestHandler):


    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data['command_loopback'] = self.path
        data['contract_num']=self.path[5:]
        # 如果command为get,如果合同号符合要求,继续
        command = self.path[0:5]
        content = self.path[5:]
        print('command:',command) 
        print('content:',content)
        if content == "":
            content = 'nodata'


    # 获取到命令，开始下一步处理#################
    ##########################################

    

    ###################command get#######################################################################
        if command == '/get/':
            print('command:',command)
            data['code']='200'
            data['detail']='success'
            # 发送数据库请求数据，数据库错误应随时中断返回错误数据
            ref_data = get_full(content)

            # 判断查询状态是否成功，成功返回数据，失败返回错误原因
            # print('查询数据结果：',ref_data)
            if ref_data[0] == True:
                # print('数据返回成功d:',ref_data[2])到这数据已经成功获取
                data['result']=ref_data[2]
                # 根据alpha jobID 开始读取订单详细信息（这里虽然已经成功获取但也应该加错误处理！）
                # print('bug:',data)
                self.wfile.write(json.dumps(data).encode())
            else:
                data['code'] = '500'
                data['detail'] = ref_data[1]
                data['result'] = ref_data[2]
                self.wfile.write(json.dumps(data).encode())

        ###########/command test#######################################################
        elif command == '/test':
            print('This is a test,recived command:',command)
            data['code']='200'
            data['detail']='Test success!'
            self.wfile.write(json.dumps(data).encode())

        ###########/unknow command###########################################################
        else:
            print('Unknow command or command error!')
            data['code']='500'
            data['detail']='Unknow command or command error!'
            self.wfile.write(json.dumps(data).encode())
            
        # 如果监测有错误返回命令不能识别,请重试

        # 命令正确，可以调用数据库查询函数处理，并把结果赋值给result，处理过程中错误把code改成错误代码

       


 
if __name__ == '__main__':
    print(sys.path)
    server = HTTPServer(host, Resquest)
    print('DASHU_ERP:请不要关闭此窗口🚀',host)


    server.serve_forever()