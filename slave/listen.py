#!/usr/bin/python
import socket
import struct
import fcntl
import subprocess
import sys
import os
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(17)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
	s.fileno(),
	0x8915, # SIOCGIFADDR
	struct.pack('256s', ifname[:15])
	)[20:24])

id = get_ip_address('eth0')

ip1, ip2, ip3, ip4 = id.split('.')

print "ID: " + ip4

#create an options file, this file should containt the parameters for the raspistill image cmd
optionfile = open('/boot/options.cfg','r')
options = optionfile.readline()
optionfile.close()
print "optons: " + options
optionfile = open('/boot/options-s.cfg','r')
optionsS = optionfile.readline()
optionfile.close()
print "optons fuer sequenzen: " + optionsS

buzzer.on()
sleep(0.1)
buzzer.off()
os.system("sudo python /boot/log.py Pi gestartet") 
while True:
	data = sock.recv(10240)
	data = data.strip()
	if data == "reboot":
		os.system("sudo python /boot/log.py Reboot") 
		print "rebooting..."
		cmd = 'reboot'
		pid = subprocess.call(cmd, shell=True)
	elif data == "poweroff":
		os.system("sudo python /boot/log.py PowerOff") 
		print "ShutDown"
		cmd = 'poweroff'
		pid = subprocess.call(cmd, shell=True)
	elif data == "info":
		print "infos:"
		cmd = 'raspistill'
		pid = subprocess.call(cmd, shell=True)
	elif data == "update":
		os.system("sudo python /boot/log.py Files werden geupdatet") 
		print "Kopiere Daten von Master\n"
		cmd = 'sudo cp -r /home/pi/files/update/* /boot/'
		pid = subprocess.call(cmd, shell=True)
		print "Update config\n"
		optionfile = open('/boot/options.cfg','r')
		options = optionfile.readline()
		optionfile.close()
		print "optons: " + options
		optionfile = open('/boot/options-s.cfg','r')
		optionsS = optionfile.readline()
		optionfile.close()
		print "optons fuer sequenzen: " + optionsS		
		print "\nReboot wird Empfohlen\n"
	elif data == "reload":
		optionfile = open('/boot/options.cfg','r')
		options = optionfile.readline()
		optionfile.close()
		print "optons: " + options
		optionfile = open('/boot/options-s.cfg','r')
		optionsS = optionfile.readline()
		optionfile.close()
		print "optons fuer sequenzen: " + optionsS
	elif data == "sequenz":
		print "shooting " + data		
		cmd = 'rm -rf ' + data
		pid = subprocess.call(cmd, shell=True)
		cmd = 'mkdir ' + data
		pid = subprocess.call(cmd, shell=True)
		cmd = 'raspistill -o ' + data + '/' + ip4 + '_%04d.jpg ' + optionsS
		pid = subprocess.call(cmd, shell=True)
		print "copy sequenz"
		cmd = 'cp -r ' + data + ' /home/pi/files/images/'
		pid = subprocess.call(cmd, shell=True)
		print "sequenz uploaded"
	elif data == "sequenz2":
		print "shooting " + data		
		cmd = 'mkdir /home/pi/files/images/' + data
		pid = subprocess.call(cmd, shell=True)
		cmd = 'raspistill -o /home/pi/files/images/' + data + '/' + ip4 + '_%04d.jpg ' + optionsS
		pid = subprocess.call(cmd, shell=True)
		print "copy sequenz"
		print "sequenz finished"
	else:
		os.system("sudo python /boot/log.py Foto wird geschossen: " + data) 
		cmd = 'mkdir /home/pi/files/images/' + data
		pid = subprocess.call(cmd, shell=True)
		print "shooting " + data		
		cmd = 'raspistill -o ' + "home/pi/files/images/" + data + "/" + data + "_" + ip4 + '.jpg ' + options
		pid = subprocess.call(cmd, shell=True)
		print "photo uploaded"
		buzzer.on()
		sleep(0.1)
		buzzer.off()
