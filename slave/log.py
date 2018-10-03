import os
import sys
import time
import socket

m = " ".join(sys.argv[1:])

def appendFile(IPaddr2log):
	timestamp= "log(" + time.strftime("%d.%m.%Y ") + " " + time.strftime("%H:%M:%S") + ")  " 
	file.write(timestamp)
	file.write("PI: " + IPaddr2log + " ")	
	file.write(": " + m)
	file.write('\n')

# file = open('file.txt','a+')
file = open('/home/pi/files/log.txt','a+')
 
# retrieve IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
id = s.getsockname()[0]
s.close()
 
	
appendFile(id)
print (m)
    
file.close()