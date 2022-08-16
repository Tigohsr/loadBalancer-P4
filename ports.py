import os, binascii, sys

# File that will store control plane table entries
s1_rules = open('lb_s1.txt', 'w')

# IPs in hex
h1 = '0a000101' # 10.0.1.1
s1 = '0a0001fe' # 10.0.1.254

h2 = '0a000202' # 10.0.2.2
h3 = '0a000303' # 10.0.3.3
h4 = '0a000404' # 10.0.4.4

# Original locations for destination from h1 to s1
orig_destinations = [h2, h3, h4]

# Original egress ports from h1 to s1
s1_ports = [2, 3, 4]

# TCP ports from 1000 to 1499
dports = range(1000,1500)

# Fixed source port to 1234
sport = '04d2' # 1234

tcp_proto = '06' # IP Protocol 

ports = []
rules = []

print(" **** Generating rules for load balancer on S1... **** ")
for dport in dports:
    # Initialize copy of original destination and ports on s1
    if len(ports) == 0:
        ports = s1_ports.copy()
        destinations = orig_destinations.copy()

    # Cryptographically secure random function to select a random port on s1
    port = int(binascii.hexlify(os.urandom(2 ** 16)), 16) % len(ports)

    # Pop port from list to provide a certain fairness during port selection
    s1_port = str(ports.pop(port))
    destination = destinations.pop(port)

    # TCP-tuple that will be hashed
    tcp_tuple = h1 + s1 + sport + format(dport,'0>4x') + tcp_proto

    # CRC32 hashing the TCP-tuple
    crc32_hash = str(binascii.crc32(binascii.a2b_hex(tcp_tuple)))

    # Append to a list the rule that will be an entry on the control plane
    rules.append('table_add lb_hash_exact lb_hash_forward ' + crc32_hash + ' => 0x' + destination + ' ' + s1_port)


# Writing list to file
s1_rules.write('\n'.join(rule for rule in rules)) 	

print(" **** Generated rules for load balancer on S1 **** ")
