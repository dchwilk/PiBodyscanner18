ifconfig eth0 10.1.0.101 netmask 255.0.0.0
printf "ip wurde zugewiesen\n"
printf "%s" "\nwarte auf MasterPi ...\n"

var=1
while [ $var > 0 ]
do
	if ping -c1 10.1.0.1 > /dev/null
	then
		printf "\nMaster Erreichbar\n"		
		printf "Ordner files wird versucht zu mounten\n"
		sudo sshfs -o nonempty pi@10.1.0.1:/home/pi/files /home/pi/files
		sleep 5s
		printf "pythonscript wird gestartet\n"
		python boot/listen.py;
		var=0
	else
		printf "\nMaster nicht erreichbar\n"
	fi
done