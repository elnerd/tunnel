import struct
import sys
import threading
import socket
import select
import requests
import time

def handle(sobj, addr, upstream_ip, upstream_port, target_ip, target_port):

    print("Connection from " + addr[0] + ":" + str(addr[1]))
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_sock.connect((upstream_ip, upstream_port))
    upstream_sock.send(socket.inet_aton(target_ip))
    upstream_sock.send(struct.pack("!H", target_port))

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


def listen_server(listen_ip, listen_port, upstream_ip, upstream_port, target_ip, target_port):
    print("Hi!")
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.bind((listen_ip, listen_port))
    print("Bound to socket")
    sobj.listen(5)
    while True:
        print("Accept loop")
        client, addr = sobj.accept()

        print("Connection from " + addr[0] + ":" + str(addr[1]))
        threading.Thread(target=handle, args=(client, addr, upstream_ip, upstream_port, target_ip, target_port)).start()

if __name__ == '__main__':
    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    upstream_ip = sys.argv[3]
    upstream_port = int(sys.argv[4])
    target_ip = sys.argv[5]
    target_port = int(sys.argv[6])

    listen_server(listen_ip, listen_port, upstream_ip, upstream_port, target_ip, target_port)