#!/usr/bin/env python3

import os
import time
import csv


class MeasureLatency:
    def __init__(self):
        # key: replica_server | val: ip address the replica server
        self.replica_servers = dict()


    '''
    Reads replica_coordinates file and store information about replica servers
    
    PARAMETERS:
        - None
    
    RETURNS:
        - None
    '''
    def read_file_to_replica_server(self):
        # global replica_coordinate
        # read the file and parse data and store
        with open('replica_coordinates.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                replica_server_ip = row['replica_server_ip']
                replica_server_name = row['replica_server']

                self.replica_servers[replica_server_name] = [replica_server_ip]

    '''
        DNS server pings all 7 replica servers 

        PARAMETERS:
            - None

        RETURNS:
            - A dictionary that contains ping time on each server
        '''
    def ping_servers(self):
        latency = dict()
        run_command_template = "scamper -c 'ping -c 1' -i {}"

        start = time.time()
        for key, value in self.replica_servers.items():
            run_command = run_command_template.format(value[0])

            # read the output directly and then parse to get avg time
            output = os.popen(run_command).read()
            output = output.split("\n")
            last_line = output[-2]
            last_line_split = last_line.split('/')
            avg = last_line_split[4]

            # store in dictionary
            latency[key] = avg
        return latency

    '''
        Gets ping time on each server constantly and writes ping times into latency.txt

        PARAMETERS:
            - None

        RETURNS:
            - None
        '''
    def write_latency_into_file(self):
        while True:
            try:
                server_latency = self.ping_servers()
                with open("latency.txt", 'w') as f:
                    for key, value in server_latency.items():
                        f.write(f'{key}: {value}\n')
                time.sleep(2)
            except:
                continue


def main():
    scamper = MeasureLatency()
    scamper.read_file_to_replica_server()
    scamper.write_latency_into_file()



if __name__ == '__main__':
    main()
