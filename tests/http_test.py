from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import socket

'''
Connecting to http server via ssh
ssh -i ~/.ssh/id_ed25519.pub promised_lan@cdn-http4.5700.network
scp -i ~/.ssh/id_ed25519.pub ~/Desktop/Northeastern\ MSCS/Courses/Spring\ 2023/CS\ 5700\ Networking/Project2/networks5700/Assignments/a5/http_test.py promised_lan@cdn-http4.5700.network:/home/promised_lan

GET /DD HTTP/1.1\r\nHost: cs5700cdnorigin.ccs.neu.edu:8080\r\n\r\n
GET /BTS HTTP/1.1\r\nHost: cs5700cdnorigin.ccs.neu.edu:8080\r\n\r\n
'''

ORIGIN_HOST = "cs5700cdnorigin.ccs.neu.edu"  # "129.10.111.154"
ORIGIN_PORT = 8080
REPLICA_SERVER_NAME = "cdn-http4.5700.network"  # "50.116.39.110"
REPLICA_SERVER_PORT = 20030

'''
Creates a socket to listens and receive client request

PARAMETERS:
    - host: the http server IP address
    - port: the http server port

RETURNS:
    - The created socket
'''
def create_recv_socket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        return s
    except Exception:
        print("Fail to create socket to listen. Retrying...")
        create_recv_socket(host, port)

'''
Creates a socket to communicate with the origin

PARAMETERS:

RETURNS:
    - The created socket
'''
def create_send_socket():
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception:
        print("Fail to create socket to send. Retrying...")
        create_send_socket()

'''
Listens incoming connection and request from clients and when client
started to communicate forward the request to the origin and grabs the
data and send back to client

PARAMETERS:
    - recv_sock: Socket that listens and receives request from clients
RETURNS:
'''
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # send a GET request to the origin server
        conn = HTTPConnection(ORIGIN_HOST, ORIGIN_PORT)
        conn.request('GET', self.path)
        resp = conn.getresponse()

        # read the response body from the origin server
        resp_body = resp.read()

        # send the response headers back to the client
        self.send_response(resp.status)
        for header, value in resp.getheaders():
            self.send_header(header, value)
        self.end_headers()

        # send the response body back to the client
        self.wfile.write(resp_body)


if __name__ == "__main__":
    replica_serv_add = (REPLICA_SERVER_NAME, REPLICA_SERVER_PORT)

    httpd = HTTPServer(replica_serv_add, MyRequestHandler)
    httpd.server_activate()
    httpd.serve_forever()

    # Need to have some sort of trigger to stop the server
    httpd.shutdown()
