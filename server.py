import socket
from _thread import *


def decrypt(data):
    print('not implemented')
    return data
def server_thread(con):
    con.send(str.encode('pajfe'))
    while True:
        data = con.recv(2048)
        reply = data.decode('utf-8')
        print(reply)
        if not data: break
        con.send(str.encode('works'))#str.encode(reply))
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