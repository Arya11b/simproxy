import socket
from _thread import *
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def decrypt(data):
    print(data)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'1',
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(b'proxyRules!'))
    f = Fernet(key)
    token = f.decrypt(bytes(data, "utf-8")).decode("utf-8")
    return token
def validate_post(req_token):
    # if req_token.find('POST') == -1: return False
    return False
def get_req_info(req):
    req_token = req.split('\n')
    body_enc = '\n'.join(req_token[req_token.index('\r') + 1:])
    body_token = decrypt(body_enc).split('\n')
    print(body_token)
    for i in body_token:
        if 'accept-encoding' in i:
            body_token.remove(i)
    url = body_token[0].split(' ')[1]
    body = '\n'.join(body_token)
    return url , body
def send_to_url(url,body):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_port = 80
    if url[-1] == '/':
        url = url[:-1]
    if 'http://' in url:
        url = url[7:]
    elif 'https://' in url:
        url = url[8:]
    if ':' in url:
        temp_url = url[:url.index(':')]
        s_port = int(url[url.index(':')+1:])
        url = temp_url
    try:
        server_socket.connect((url,s_port))
        server_socket.send(str.encode(body))
    except socket.error as e:
        print(str(e))
        sys.exit(1)
    reply = []
    while True:
        try:
            server_socket.settimeout(3.0)
            data = server_socket.recv(2048)
            try:
                reply.append(data)
            except UnicodeDecodeError as u:
                pass
        except socket.timeout as e:
            break
    return b''.join(reply)
def server_thread(con):
    data = con.recv(4096)
    reply = data.decode('UTF-8')
    # print(req)
    url, body = get_req_info(reply)
    res = send_to_url(url,body)
    print('yay')
    print(res)
    con.send(res)
    print('yay 2')
    con.close()
host = ''
port = 8080
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((host,port))
    s.listen(5)
except socket.error as e:
    print(str(e))
while True:
    con, addr = s.accept()
    print('connected to {0}:{1}'.format(addr[0],addr[1]))
    start_new_thread(server_thread,(con,))