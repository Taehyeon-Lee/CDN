import socket
import time

REPLICA_SERVER_NAME = "cdn-http1.5700.network"  # "50.116.39.110"

def client_program():
    host = socket.gethostbyname(REPLICA_SERVER_NAME)  # as both code is running on same pc
    port = 20030  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    request = b"GET /Israel HTTP/1.1\r\nHost: cs5700cdnorigin.ccs.neu.edu:8080\r\n\r\n"
    client_socket.sendall(request)

    response = b""
    while True:
        data = client_socket.recv(2048)
        response += data
        print(data)
        if b"</html>" in data:
            break
        if not data:
            break
        # print(data)

    # with open("BTS_test.html", 'wb') as f:
    #     f.write(response)

    client_socket.close()  # close the connection
    return response


if __name__ == '__main__':
    times = []

    i = 0
    while i < 1:
        start = time.time()
        data = client_program()
        end = time.time()
        times.append(end - start)
        print(i)
        print(data)
        i += 1

    print(f"\n\nAverage runtime over 50 runs: {sum(times) / len(times)}\n\n")

    # 50 times in a row cleopatra uncompressed cache avg: 0.29540921211242677 seconds/request
    # 50 times in a row cleopatra compressed to decompressed cache avg: 0.2947140884399414 seconds/request
    # rm cleo from cache and force replica to go to origin: 0.6051391983032226
    # 50 times a file not in cache - YouTube - from origin: 0.7179362154006959
    # 50 times a file in cache - YouTube - NOT compressed: 0.6700294780731201
    # 50 times a file in cache - YouTube - IS compressed and we decompress first: 0.6700294780731201
    # first time YT not in cache, then next times its compressed in ram cache and we decomp before sending: 0.3683988094329834
    # without decompressing: 0.6315401744842529



# cleo zipped from cache = 0.3     then unzip from cache before sending 0.2
# dd zipped from cache = 0.02      then unzip from cache before sending 0.08
# dd not zipped from origin = 0.03  then unzip before sending from origin 0.05

# israel not cached and unzipped = 0.2 | 0.2
# then from cache and zipped = 0.1 THEN from cache unzipped = 0.2