from http import server
import sys
from http.server import HTTPServer,BaseHTTPRequestHandler,SimpleHTTPRequestHandler
import json

host = ('127.0.0.1',8888)
data = {'code':'200'}


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        print(self.path)
        data['data'] = 'datas'

        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length'])) #重点在此步!
        print(req_datas.decode())
        data = {
            'result_code': '2',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()



if __name__ == '__main__':
    server = HTTPServer(host,Resquest)
    server.serve_forever()