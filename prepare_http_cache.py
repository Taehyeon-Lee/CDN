#!/usr/bin/env python3

import gzip
import os
import socket
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection

REPLICA_SERVER_NAME = socket.gethostname()
REPLICA_IP = socket.gethostbyname(REPLICA_SERVER_NAME)
PORT = 20039


alert_mapping = {       # mst paths for forwarding ram cache alerts
    "3": ["4"],
    "4": ["1", "3"],
    "1": ["4", "7"],
    "7": ["1", "6"],
    "6": ["5", "7"],
    "5": ["2", "6"],
    "2": ["5"],
}


'''
Cascades POST messages to the next replica server in the MST of servers so they can cache a file that should be 
in their file system cache.

PARAMETERS:
    - target_file: the name of the file to cache
    - compressed_len: the len of the compressed version of the file
    - compressed_body: the compressed byte string of the text
    - received_from: the IP address of the previous hop according to the MST of replica servers

RETURNS:
    - None
'''
def cascade_to_other_replicas(target_file, compressed_len, compressed_body, received_from):
    if received_from != REPLICA_IP:
        replica_base_start = "cdn-http"
        replica_base_end = ".5700.network"
        curr_node = REPLICA_SERVER_NAME[len(replica_base_start):len(replica_base_start)+1]
        # pass the info to the next replica node in the mst
        # (but not to the node that sent it to this current node)
        for node in alert_mapping[curr_node]:
            dest_name = replica_base_start + node + replica_base_end
            dest_addr = socket.gethostbyname(dest_name)
            if dest_addr != received_from:
                try:
                    conn = HTTPConnection(dest_addr, PORT)
                    headers = {"Content-Encoding": "gzip", "compressed_len": str(compressed_len)}

                    conn.request('POST', "/file_dongle/" + target_file,
                                 body=compressed_body, headers=headers)
                except:
                    pass


'''
Handles HTTP query communication through TCP between client and origin server
'''
class MyRequestHandler(BaseHTTPRequestHandler):
    '''
    Listens for incoming POST messages from fellow servers reporting file system cached material.
    Stores the zipped file in its file system cache and then forwards the file to the next hop(s) in the MST.

    PARAMETERS:
        - None

    RETURNS:
        - None
    '''
    def do_POST(self):
        try:
            # parse for file name
            target_file = self.path[1:]
            target_file = target_file[target_file.index("file_dongle/") + len("file_dongle/"):]
            # check if file is from another replica for caching
            if self.path == "/file_dongle/" + target_file:
                compressed_len = int(self.headers.get("compressed_len"))
                compressed_body = b''
                while True:
                    chunk = self.rfile.read(1024)
                    if not chunk:
                        break
                    compressed_body += chunk

                # add the file to file cache IF not corrupted
                # and cascade to the next node in mst
                if compressed_len == len(compressed_body) and not os.path.isfile(target_file + ".gz"):
                    with open(target_file + ".gz", 'wb') as file:
                        file.write(compressed_body)
                    # send to the next node in mst
                    cascade_to_other_replicas(target_file, compressed_len, compressed_body, self.client_address[0])
                compressed_body = b''
        except:
            pass


'''
Requests all file system cache files from the origin and then
cascades the data to the remaining replica servers

PARAMETERS:
    - None

RETURNS:
    - None
'''
def set_up_cache():
    output_path = "./"
    with open("urls.txt", 'rb') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            if i < 205:
                # get page title and fix spacing
                url = row.decode().strip()
                page = url.rsplit('/', 1)[-1]
                if page == "-":
                    continue
                # wget the file, zip it, and store in server file system
                try:
                    command = f"wget -q {url} -P {output_path} -O {page}"
                    os.system(command)
                except:
                    continue
                try:
                    with open(page, 'rb') as f_in:
                        with gzip.open(page + '.gz', 'wb') as f_out:
                            f_out.writelines(f_in)
                    # remove unzipped version
                    os.remove(page)
                except:
                    continue
                try:
                    # start the cascade forwarding to the remaining replica servers
                    with open(page + ".gz", 'rb') as f:
                        body_out = f.read()
                    cascade_to_other_replicas(page, os.path.getsize(page + ".gz"), body_out, None)
                    body_out = b''
                except:
                    continue
            else:
                break


'''
Starts the cascade of server file system cache population.
Starts at node 1 and follows the MST path to fill all replica file system caches
without overloading the origin with requests

PARAMETERS:
    - None

RETURNS:
    - None
'''
def start_cascade():
    if REPLICA_SERVER_NAME == "cdn-http1.5700.network":
        set_up_cache()


'''
Gets the 4 outlier files on the remaining 6 replica nodes that cannot be sent via POST due to character errors

PARAMETERS:
    - None

RETURNS:
    - None
'''
def get_outliers():
    outliers = ["cs5700cdnorigin.ccs.neu.edu:8080/Dahmer_–_Monster:_The_Jeffrey_Dahmer_Story",
                "cs5700cdnorigin.ccs.neu.edu:8080/Brahmāstra:_Part_One_–_Shiva",
                "cs5700cdnorigin.ccs.neu.edu:8080/Gisele_Bündchen",
                "cs5700cdnorigin.ccs.neu.edu:8080/Luiz_Inácio_Lula_da_Silva"]
    output_path = "./"

    if REPLICA_SERVER_NAME != "cdn-http1.5700.network":
        for outlier in outliers:
            page = outlier.rsplit('/', 1)[-1]
            # wget the file, zip it, and store in server file system
            try:
                command = f"wget -q {outlier} -P {output_path} -O {page}"
                os.system(command)
            except:
                continue
            try:
                with open(page, 'rb') as f_in:
                    with gzip.open(page + '.gz', 'wb') as f_out:
                        f_out.writelines(f_in)
                # remove unzipped version
                os.remove(page)
            except:
                continue


if __name__ == '__main__':
    # bundle replica server's address
    replica_serv_add = (REPLICA_SERVER_NAME, PORT)

    # start servers
    http = HTTPServer(replica_serv_add, MyRequestHandler)
    http.server_activate()

    # start a new thread to run the server forever
    server_thread = threading.Thread(target=http.serve_forever)
    server_thread.start()

    # get outliers during the timeout while all replicas start their servers
    # and begin the cascade of cache population
    get_outliers()
    time.sleep(15)
    start_cascade()

    # wait for cache population to complete then free resources
    time.sleep(200)

    # shutdown the server
    http.shutdown()
    http.server_close()

    # join the server thread to wait for it to finish
    server_thread.join()

    sys.exit()
