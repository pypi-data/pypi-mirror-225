from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class _Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write()

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        print("do post:", self.path, self.client_address, datas)
        msg = json.loads(datas)
        _hasmsg(msg)
def _listen(host):
    server = HTTPServer(host, _Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
def _hasmsg(msg):
    print(msg["message"])