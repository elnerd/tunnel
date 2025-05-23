import struct
import threading
import socket
import time
import sys
import select


def handle(sobj, addr):
    target_ip = socket.inet_ntoa(sobj.recv(4))
    target_port = struct.unpack('!H', sobj.recv(2))[0]
    print(target_ip, target_port)
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_sock.connect((target_ip, target_port))
    while True:
        ready_to_read, _, _ = select.select([upstream_sock, sobj], [], [])
        if sobj in ready_to_read:
            data = sobj.recv(1024)
            sent = 0
            while sent < len(data):
                sent += upstream_sock.send(data[sent:])

        if upstream_sock in ready_to_read:
            data = upstream_sock.recv(1024)
            sent = 0
            while sent < len(data):
                sent += sobj.send(data)
        time.sleep(1)

def listen_server(listen_ip, listen_port):
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.bind((listen_ip, listen_port))
    sobj.listen(5)
    while True:
        client, addr = sobj.accept()
        threading.Thread(target=handle, args=(client, addr)).start()

if __name__ == '__main__':
    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])


    listen_server(listen_ip, listen_port)