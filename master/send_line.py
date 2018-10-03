import socket
import sys
import time
import subprocess

print 'photo name:' + sys.argv[1]

if sys.argv[1] == "update":
	print "Kopiere Daten in das Austauschverzeichnis\n"
	cmd = 'sudo cp -r /boot/update/* /home/pi/files/update/'
	pid = subprocess.call(cmd, shell=True)
	print "\nUpdate wird auf die Pi's gespielt\n"

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

sock.setsockopt(socket.SOL_SOCKET, 25, 'eth0')

sock.sendto(sys.argv[1], (MCAST_GRP, MCAST_PORT))
