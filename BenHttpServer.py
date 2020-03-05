import socket
from threading import Thread
## add request handler
## todo how to implement  keep-alive connection
## /favicon.ico
import os
class HttpRequest:
    def __init__(self):
        self.version = None
        self.method = None
        self.path = None
        self.content_type = None
        self.content_length = None
        self.host = None
        self.connection = None
        self.user_agent = None


def send_header(con, keyword, value):
    data = "%s: %s\r\n".format(keyword, value)
    con.send(data)

def end_head(con):
    con.send("\r\n")
def do_post():
    pass

def parse_http_request(req_msg):
    httprequest = HttpRequest()
    method_path_version = req_msg.split('\r\n')[0].split(' ')

    method = method_path_version[0]
    path = method_path_version[1]
    version = method_path_version[2]
    httprequest.method = method
    httprequest.path = "." + path
    httprequest.version = version
    print("path in http request:" + path)

    return httprequest

def do_get(conn):
    from_b_msg = conn.recv(1024)
    str_msg = from_b_msg.decode('utf-8')
    print(str_msg)
    httprequet = parse_http_request(str_msg)

    if os.path.exists(httprequet.path):
        send_file(conn, httprequet)
    else:
        send_error(conn, httprequet)

def send_file(conn, httprequest):
    path = httprequest.path
    data = None
    print(path)
    with open(path) as f:
        data = f.read()
    print(data)

    conn.send(b'HTTP/1.1 200 ok \r\n')
    send_header(conn, "Content-type", "text/html")
    send_header(conn, "Content-Length", str(len(data)))
    end_head(conn)

    conn.send(data)
    conn.close()

def send_error(conn, httprequest):
    path = "./error.html"
    data = None
    with open(path) as f:
        data = f.read()
    print(data)

    conn.send(b'HTTP/1.1 404 Not Found\r\n')
    send_header(conn, "Content-type", "text/html")
    send_header(conn, "Content-Length", str(len(data)))
    end_head(conn)

    conn.send(data)
    conn.close()


class BenHttpServer:
    def __init__(self, ip, port):
        self.sk = self._create_socket(ip, port)

    def _create_socket(self, ip, port):
        sk = socket.socket()
        sk.bind((ip, port))
        sk.listen(5)
        return sk

    def serve(self):
        while True:
            conn,addr = self.sk.accept()
            ## todo here implement a thread pool is a more efficient way
            t=Thread(target=do_get, args=(conn,))
            t.start()

if __name__ == '__main__':
    server = BenHttpServer('127.0.0.1', 8080)
    server.serve()
