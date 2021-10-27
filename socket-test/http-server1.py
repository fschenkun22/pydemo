
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
 
data = {'code':'200','detail':'request passed!'}
host = ('0.0.0.0', 8888)
 
class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        data['result'] = self.path
        data['new'] = 'test'
        self.wfile.write(json.dumps(data).encode())
        print(self.path)


 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    # print("Starting server, listen at: %s:%s" % host)
    print('DASHU_ERP:请不要关闭此窗口',host)
    server.serve_forever()