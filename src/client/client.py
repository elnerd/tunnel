import socket
import time

import requests

import socket
import select
import requests
import time

URL = "http://127.0.0.1:5000/webshell"

TARGET_HOST = "mapscii.me"
TARGET_PORT = 23

def handle(sobj, addr):
    session_id = int(time.time())
    session = requests.Session()
    print("Handling", addr)
    resp = session.post(URL,
                        params={"cmd": "CONNECT", "host": TARGET_HOST, "port": TARGET_PORT, "id": session_id})
    print(resp.headers)
    # time.sleep(3)

    sobj.setblocking(True)  # If it blocks, our selects are wrong

    got_data = True
    while True:
        if not got_data:
            time.sleep(1)
        got_data = False

        ready_to_read, _, _ = select.select([sobj], [], [], 0)  # setting timeout to 0 for non-blocking operation
        if ready_to_read:  # if sobj is ready for reading
            data = sobj.recv(1024)
            if not data:
                print("Client has disconnected.")
                session.post(URL, params={"cmd": "DISCONNECT", "id": session_id})
                return
        else:
            data = b""

        resp = session.post(URL, params={"cmd": "COMM", "id": session_id}, data=data)
        cmd_resp = resp.headers.get("X-STATE", "FAILED")
        if cmd_resp != "OK":
            print("Disconnecting", resp.content)
            return

        try:
            data = resp.content
            sent = 0
            while sent < len(data):
                sent += sobj.send(data[sent:])

            if sent > 0:
                got_data = True

        except BrokenPipeError:  # if send() raises a BrokenPipeError, the client has disconnected
            print("Client has disconnected.")
            return



def listen_server():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.bind(('127.0.0.1', 9999))
    sobj.listen(5)
    client, addr = sobj.accept()
    handle(client, addr)

if __name__ == '__main__':
    listen_server()