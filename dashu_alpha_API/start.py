
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
 
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

        if command == '/get/':
            print('command:',command)
            data['code']='200'
            data['detail']='success'
            # 发送数据库请求数据，数据库错误应随时中断返回错误数据
            self.wfile.write(json.dumps(data).encode())

        else:
            print('command error')
            data['code']='500'
            data['detail']='command error'
            self.wfile.write(json.dumps(data).encode())
            
        # 如果监测有错误返回命令不能识别,请重试

        # 命令正确，可以调用数据库查询函数处理，并把结果赋值给result，处理过程中错误把code改成错误代码

       


 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print('DASHU_ERP:请不要关闭此窗口🚀',host)3


    server.serve_forever()