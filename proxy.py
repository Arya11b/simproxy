import socket
import requests

from _thread import *
host = ''
port = 5555
server_host = 'localhost'
server_port = 8080
def post_to_server(body):
    # print('ni')
    print(body)
    requests.post('http://{0}:{1}'.format(server_host, server_port), body)
def encrypt(text):
    print('enc not implemented')
    return text
def client_thread(con):
    con.send(str.encode('hello there!'))
    while True:
        data = con.recv(2048)
        reply = data.decode('utf-8')
        enc_data = encrypt(reply)
        post_to_server(enc_data)
        if not data: break
        con.send(str.encode('works'))#str.encode(reply))
    con.close()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((host,port))
    s.listen(5)
except socket.error as e:
    print(str(e))
while True:
    con, addr = s.accept()
    print('connected to {0}:{1}'.format(addr[0],addr[1]))
    start_new_thread(client_thread,(con,))