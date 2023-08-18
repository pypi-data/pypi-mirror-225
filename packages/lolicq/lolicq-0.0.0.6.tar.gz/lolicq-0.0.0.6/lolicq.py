from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

posturl = ('127.0.0.1',5700)#Cqhttp监听地址
listurl = ('127.0.0.1',5701)#Lolicq监听地址
def launch():
    _listen(listurl)
def sendgm(gid,text):
    url = ('http://'+str(posturl[0])+':'+str(posturl[1])+'/')
    data = {'group_id':gid,'message':text}
    _sendpost(url+'send_group_msg',json.dumps(data))
def sendpm(uid,text):
    url = ('http://'+str(posturl[0])+':'+str(posturl[1])+'/')
    data = {'user_id':uid,'message':text}
    _sendpost(url+'send_private_msg',json.dumps(data))
def pmsg(uid,text):
    pass
def gmsg(gid,uid,text):
    pass

class _Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write()

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        msg = json.loads(datas)
        if msg['post_type'] == 'message':
            _hasmsg(msg)
        self.send_response_only(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(''.encode())
    
def _listen(host):
    server = HTTPServer(host, _Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
def _hasmsg(msg):
    if msg['message_type'] == 'private':
        pmsg(msg['user_id'],msg['message'])
    else:
        gmsg(msg['group_id'],msg['user_id'],msg['message'])

def _sendpost(point,tex):
    url = point
    data = json.dumps(tex)
    return requests.post(url=url,data=data)