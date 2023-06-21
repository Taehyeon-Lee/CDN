#!/usr/bin/env python3

from dnslib import *
import socket


DNS_SERVER_NAME = "cdn-dns.5700.network"
DNS_SERVER_PORT = 20030
REPLICA_SERVER_1_NAME = "cdn-http4.5700.network"
ORIGIN_SERVER_NAME = "http://cs5700cdnorigin.ccs.neu.edu"
ORIGIN_SERVER_PORT = 8080
SERVING_DOMAIN_NAME = "cs5700cdn.example.com."
GOOGLE_PUBLIC_DNS = "8.8.8.8"

# key: location | val: ip of replica server
ip_table = {}


'''
Creates a socket for receiving UDP packets

PARAMETERS:
	- host: the server IP address
	- port: the port that the server is listening on

RETURNS:
	- The created UDP receive socket
'''
def create_receive_UDP_socket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        print(f"[+] Receive socket successfully bound to IP: {host} | port: {port}")
        return sock

    except Exception:
        print("[-] An error occurred while attempting to create the receive UDP socket. Retrying...")
        create_receive_UDP_socket(host, port)


'''
Creates a socket for sending UDP packets

PARAMETERS:
	- None

RETURNS:
	- The created UDP send socket
'''
def create_send_UDP_socket():
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    except Exception:
        print("[-] An error occurred while attempting to create the send UDP socket. Retrying...")
        create_send_UDP_socket()


'''
Builds an unpacked DNS response to a received DNS query.
(If the query is out of the CDN domain, responds with RCODE.REFUSED)

PARAMETERS:
	- data: the raw DNS request packet received from the client
	- ip: the IP address for the repsonse (received from ip_table)

RETURNS:
	- reply: the unpacked DNS response
'''
def build_response(data, ip):
    try:
        # parse query
        query = DNSRecord.parse(data)
        # grab domain from query
        domain = query.q.qname
        print(f"[+] Client is attempting to reach {domain}")

        # build dns reply
        reply = query.reply()

        # validate domain
        if domain != SERVING_DOMAIN_NAME:
            reply.header.rcode = RCODE.REFUSED
            print("[-] Client is requesting a domain that is outside of our CDN...")
        else:
            reply.add_answer(RR(domain, QTYPE.A, rdata=A(ip), ttl=60))
            print(f"[+] Replying with DNS server address: " + ip)

        return reply

    except:
        exit("An error occurred while attempting to build the DNS response. Exiting...")


# Main execution flow
def main():
    # grab server IPs
    dns_server_ip = socket.gethostbyname(DNS_SERVER_NAME)
    replica_server_1_ip = socket.gethostbyname(REPLICA_SERVER_1_NAME)

    # add replica server(s) to IP table
    ip_table["any"] = replica_server_1_ip

    # open send/receive sockets
    receive_sock = create_receive_UDP_socket(dns_server_ip, DNS_SERVER_PORT)
    send_sock = create_send_UDP_socket()

    # listen for DNS queries
    while True:
        print("------------------------------------------------------------")
        # receive a message from a client
        dns_bytes, requester_addr = receive_sock.recvfrom(1024)
        print(f"[+] Connected with client: {requester_addr}")

        # for debugging - delete later ###########################
        response = build_response(dns_bytes, ip_table["any"])
        print("\n\nResponse:")
        print(response)
        print()
        print()
        ##########################################################

        # send response
        try:
            send_sock.sendto(response.pack(), requester_addr)
            print(f"[+] DNS response sent to {requester_addr}")

        except:
            print(f"An error occurred while attempting to respond to {requester_addr}")


if __name__ == '__main__':
    main()
