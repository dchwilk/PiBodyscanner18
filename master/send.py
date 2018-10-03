import socket
import sys
import time

while True:
	print 'photo name:'
	n = sys.stdin.readline()
	n = n.strip('\n')

	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	sock.sendto(n, (MCAST_GRP, MCAST_PORT))