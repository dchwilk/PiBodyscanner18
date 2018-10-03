#!/usr/bin/python
import socket
import struct
import subprocess
import sys
import os
import time

i = 0
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

time.sleep(10)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock2.setsockopt(socket.SOL_SOCKET, 25, 'eth0')

print "\nWarte auf Server...\n"

os.system("sudo python /boot/log.py Master gestartet") 

while i < 1:
	data = sock.recv(10240)
	data = data.strip()
	if data == "reboot":
		os.system("sudo python /boot/log.py Pi startet neu") 
		print "Reboote KameraPis herunter...\n"
		sock2.sendto(data, (MCAST_GRP, MCAST_PORT))
		print "rebooting..."
		cmd = 'reboot'
		pid = subprocess.call(cmd, shell=True)
	elif data == "poweroff":
		os.system("sudo python /boot/log.py Pi geht aus") 
		print "Fahre KameraPis herunter...\n"
		sock2.sendto(data, (MCAST_GRP, MCAST_PORT))
		print "ShutDown"
		cmd = 'poweroff'
		pid = subprocess.call(cmd, shell=True)
	elif data == "update":
		os.system("sudo python /boot/log.py Pis erhalten neue Version") 
		print "Update Pis"
		print "Kopiere Daten in das Austauschverzeichnis\n"
		cmd = 'sudo cp -r /boot/update/* /home/pi/files/update/'
		pid = subprocess.call(cmd, shell=True)		
		sock2.sendto(data, (MCAST_GRP, MCAST_PORT))
		print "\nUpdate wird auf die Pi's gespielt\n"
	elif data == "stop":
		os.system("sudo python /boot/log.py Master-Script schliesst") 
		i = 1
	else:
		sock2.sendto(data, (MCAST_GRP, MCAST_PORT))
		print "shooting " + data
		os.system("sudo python /boot/log.py Bilder erstellt mit Namen: " + data) 
		print "Fotoupload ist noch nicht Implementiert"
