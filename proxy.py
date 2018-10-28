import socket
import requests
from _thread import *
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
host = ''
port = 5555
key = '!!#pp73281'
server_host = 'localhost'
server_port = 8080
def recv_data(con):
    reply = []
    while True:
        try:
            con.settimeout(2.0)
            data = con.recv(2048)
            reply.append(data)
        except socket.error as e:
            break
    reply = b''.join(reply)
    print(reply)
    return reply
def post_to_server(body):
    return requests.post('http://{0}:{1}'.format(server_host, server_port), body)
def encrypt(text):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'1',
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(b'proxyRules!'))
    f = Fernet(key)
    text = f.encrypt(bytes(text, "utf-8")).decode("utf-8")
    return text
def client_thread(con,eh,ep):
    data = con.recv(4096)
    reply = data.decode('utf-8')
    enc_data = encrypt(reply)
    res = post_to_server(enc_data)
    res_plain = 'HTTP/1.1 {status_code}\n\n{body}'.format(
        status_code= res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.text,
    )
    print(res_plain)
    con.sendall(res_plain.encode())
    con.close()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((host,port))
    s.listen(10)
except socket.error as e:
    print(str(e))
while True:
    con, addr = s.accept()
    print('connected to {0}:{1}'.format(addr[0], addr[1]))
    end_host = addr[0]
    end_port = addr[1]
    start_new_thread(client_thread, (con,end_host,end_port,))