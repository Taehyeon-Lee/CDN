from dnslib import DNSRecord, DNSQuestion, QTYPE, CLASS, A, DNSError
import socket

neu_dns = "cdn-dns.5700.network"
neu_dns_ip = socket.gethostbyname(neu_dns)
neu_rep_server = "cdn-http4.5700.network"
DNS_SERVER_NAME = "cdn-dns.5700.network"
DNS_SERVER_PORT = 20030


def create_receive_UDP_socket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        print(f"[+] Receive socket successfully bound to IP: {host} | port: {port}")
        return sock

    except Exception:
        print("[-] An error occurred while attempting to create the receive UDP socket. Retrying...")
        create_receive_UDP_socket(host, port)



# Set up DNS query
qname = "cs5700cdn.example.com"
q = DNSRecord.question(qname)

print(f"DNS Query:\n{q}\n\n")

DNS_ip = socket.gethostbyname(DNS_SERVER_NAME)

h = socket.gethostname()
i = socket.gethostbyname(h)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(q.pack(), (DNS_ip, DNS_SERVER_PORT))

# Receive response from DNS server
print(s.getsockname()[1])
rs = create_receive_UDP_socket(i, s.getsockname()[1])
response, _ = rs.recvfrom(1024)

# Parse response using dnslib
response_record = DNSRecord.parse(response)
print(f"DNS Response:\n{response_record}\n\n")

answers = response_record.rr
print(f"Answers:\n{answers}\n\n")
ip_addresses = [answer.rdata for answer in answers if answer.rtype == QTYPE.A]

# Print IP addresses
print(f"IP addresses for {qname}: {ip_addresses}")
