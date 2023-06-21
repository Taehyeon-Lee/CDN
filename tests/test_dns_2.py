import socket
import socketserver
from dnslib import DNSRecord, QTYPE


DNS_SERVER_NAME = "cdn-dns.5700.network"


# class UDPHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         # create a DNS request packet for a TXT record
#         qname = "example.com."
#         q = DNSRecord.question(qname, QTYPE.TXT)
#
#         # send the request as a UDP message to 1.2.3.4:20030
#         sock = self.request[1]
#         sock.sendto(bytes(q.pack()), ('1.2.3.4', 20030))


DNS_ip = socket.gethostbyname(DNS_SERVER_NAME)
# create a socket and send the DNS query to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
qname = "example.com."
q = DNSRecord.question("abc.com", "MX")
sock.sendto(bytes(q.pack()), (DNS_ip, 20030))

# wait for the response
response, address = sock.recvfrom(4096)
print(DNSRecord.parse(response))
