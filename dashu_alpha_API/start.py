
import print_fun.printv1 as printv1
from common.read_full_contract_num import get_full
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
import time
import ntplib
import cgi
import urllib.parse
import urllib.request
import re


from common.write_contract import write_contract_by

sys.path.append("./common/")
sys.path.append("./print_fun/")
# 载入print_fun

data = {'code': '200'}
host = ('0.0.0.0', 65500)


class Resquest(BaseHTTPRequestHandler):

 ####### POST functions##################
    def do_POST(self):
        data_post = {}
        # 获取post提交的数据
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        print('ctype:', ctype)
        print('pdict:', pdict)
        dt = self.rfile.read(int(self.headers['content-length']))
        print('dt:', dt)
        # dt现在返回是上面那样，从里面解析出 key 和 value
        pattern = r'name="(\w+)"\r\n\r\n(\w+)'
        result = re.findall(pattern, dt.decode('utf-8'))
        # 结果非常完美result: [('text1', '222'), ('text2', '555')]
        print('result:', result)

        # 从结果中提取指定的值
        for i in result:
            if i[0] == 'qr_code':
                data_post['qr_code'] = i[1]
            elif i[0] == 'text1':
                data_post['text1'] = i[1]
            elif i[0] == 'text2':
                data_post['text2'] = i[1]
            elif i[0] == 'text3':
                data_post['text3'] = i[1]

        res = printv1.print_full(
            qr_code=data_post['qr_code'],
            text1=data_post['text1'],
            text2=data_post['text2'],
            text3=data_post['text3']
        )

        print('data_post:', data_post)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Hello, POST request received!".encode('utf-8'))

        if res == '打印成功':
            print('写入通过')
            data_post['code'] = 200
            data_post['status'] = True
            data_post['msg'] = 'write done'
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data_post).encode())

        else:
            print('可能是测试或者写入失败',res)
            data_post['code'] = 500
            data_post['status'] = False
            data_post['msg'] = 'write fail'
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data_post).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data['command_loopback'] = self.path
        data['contract_num'] = self.path[5:]
        # 如果command为get,如果合同号符合要求,继续
        command = self.path[0:5]
        content = self.path[5:]
        print('command:', command)
        print('content:', content)
        if content == "":
            content = 'nodata'

    # 获取到命令，开始下一步处理#################
    ##########################################
    ################### command get#######################################################################
        if command == '/get/':
            print('command:', command)
            data['code'] = '200'
            data['detail'] = 'success'
            # 发送数据库请求数据，数据库错误应随时中断返回错误数据
            ref_data = get_full(content)

            # 判断查询状态是否成功，成功返回数据，失败返回错误原因
            # print('查询数据结果：',ref_data)
            if ref_data[0] == True:
                # print('数据返回成功d:',ref_data[2])到这数据已经成功获取
                data['result'] = ref_data[2]
                # 根据alpha jobID 开始读取订单详细信息（这里虽然已经成功获取但也应该加错误处理！）
                # print('bug:',data)
                self.wfile.write(json.dumps(data).encode())
            else:
                data['code'] = '501'
                data['detail'] = ref_data[1]
                data['result'] = ref_data[2]
                self.wfile.write(json.dumps(data).encode())
        ########### /command test#######################################################
        elif command == '/test':
            print('This is a test,recived command:', command)
            data['code'] = '200'
            data['detail'] = 'Test success!'
            data['result'] = {}
            # time.sleep(10)
            self.wfile.write(json.dumps(data).encode())
        ########### /unknow command###########################################################
        else:
            print('Unknow command or command error!')
            data['code'] = '500'
            data['detail'] = 'Unknow command or command error!'

            self.wfile.write(json.dumps(data).encode())

        # 如果监测有错误返回命令不能识别,请重试
        # 命令正确，可以调用数据库查询函数处理，并把结果赋值给result，处理过程中错误把code改成错误代码
# end do get
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()


############ PUT functions##################

    def do_PUT(self):
        data_put = {}
        ref_data = {}
        self.headers['content-length']
        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len)
        print("command str :", self.path)
        ref_data = write_contract_by(self.path)

        if ref_data['status'] == True:
            print('写入通过')
            data_put['code'] = 200
            data_put['status'] = True
            data_put['msg'] = 'write done'
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data_put).encode())

        else:
            print('写入失败')
            data_put['code'] = 500
            data_put['status'] = False
            data_put['msg'] = ref_data['msg']
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data_put).encode())


if __name__ == '__main__':
    # print(sys.path)
    res = ntplib.NTPClient().request('ntp.aliyun.com')
    # print(res.tx_time)
    if res.tx_time < 1872498100:
        server = HTTPServer(host, Resquest)
        print('DASHU_ERP:请不要关闭此窗口🚀', host)

        server.serve_forever()
    else:
        print('大树ERP：授权已到期 请联系客服 15641366461')
        time.sleep(1200)
        exit()
