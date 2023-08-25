
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
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QThread, Signal, Slot, QSize
# 异步需要的函数载入threading
import threading

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
        pattern = r'name="(.+?)"\r\n\r\n(.+?)\r\n'
        result = re.findall(pattern, dt.decode('utf-8'))
        print('result⚠️:', result)
        # 在textEdit上输出result
        window.thread_1.call_back(
            '<font color="#595">Print cmd : </font>' + str(result)
        )

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

        print('data_post:', res)

        if res['code'] == 200 or res['code'] == 201:
            window.thread_1.call_back(
                '<font color="green">' + 'print job finished : ' +
                str(res['msg']) + '</font>'
            )

            print('写入通过')
            data_post['code'] = 200
            data_post['status'] = True
            data_post['msg'] = '发送打印信号打印完毕'

            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            window.thread_1.call_back(
                '<font color="red">Print Error</font>' + str(res)
            )
            data_post = res
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")

            print('data_post 准备返回请求头', data_post)
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
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        print('end headers')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):

        self.send_response(200, "ok")
        self.end_headers()

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


class Mythread_1(QThread):
    # 可以调用Mythread_1的call_back函数回显数据
    signal_tuple = Signal(tuple)

    def __init__(self):
        super().__init__()

    def run(self):
        server = HTTPServer(host, Resquest)
        self.call_back('<font color="#595">Server start </font>')
        server.serve_forever()

    def call_back(self, data):
        self.signal_tuple.emit(data)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        qfui = QFile('./start.ui')
        qfui.open(QFile.ReadOnly)
        qfui.close()
        self.ui = QUiLoader().load(qfui)
        # 绑定槽
        self.ui.pushButton.clicked.connect(self.setup_thread_1)
        self.ui.pushButton_2.clicked.connect(self.quit_thread_1)
        # self.ui.textEdit.append("hello world")

    def on_button_click(self):
        # 禁用按键1
        pass
        

    def on_button_click2(self):
        print("Button clicked2!")

    def setup_thread_1(self):
        # 禁用按键
        self.ui.pushButton.setEnabled(False)
        self.thread_1 = Mythread_1()
        self.thread_1.signal_tuple.connect(self.thread_1_finished)
        self.thread_1.start()

    # 销毁thread_1
    def quit_thread_1(self):
        self.thread_1.terminate()
        self.ui.textEdit.append('<font color="#f00"> thread terminated </font>')

    def test(self):
        print('test')

    @Slot(tuple)
    def thread_1_finished(self, item):
        print('接收到子线程1结束信号:', item)
        self.ui.textEdit.append(
            str(item)
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    app.exec()
