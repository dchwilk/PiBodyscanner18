#!/bin/bash
ifconfig eth0 10.1.0.1 netmask 255.0.0.0
printf "\nip gesetzt\n"
printf "pythonscript wird gestartet\n"
/usr/bin/python /boot/listen_master.py
