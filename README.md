# Raspberry Pi 3D Bodyscanner

Die Raspberry Pi Kamera gehört zu den günstigsten Digitalkameras. Nahezu konkurenzlos wird dieser wenn der anspruch über das einfache Fotomachen hinaus geht.
Das Ziel dieses Projektes ist die Realisierung eines 3D-Bodyscanners welche in seiner größe problemfrei erweiterbar ist.

Dieses Projekt ist dabei mitinspiriert von Folgendem Projekt:
https://www.instructables.com/id/Multiple-Raspberry-PI-3D-Scanner/

Dabei erstellen die Pis nur die Bilder welche seperat mittels SFM verarbeitet werden.

Anders als vergleichbare Projekte abeitet dieses Projekt mit einer herahierung. Ein Master-Pi steuert n-viele Slave-Pis. So können getrennte einheiten aufgebaut werden und ein Mesh von Scannern können gemeinschaftlich Fotos erstellen. dabei ist jede einheit für sich frei Positionierbar.


#Installation

Für dieses Projekt wurde Raspian verwendet. Allerdings ist jedes Raspbery-OS denkbar sollange Python 2.7 und die Pi Kamera unterstützt wird.
Des weiteren muss SSHFS installiert sein und auf jedem Pi der passende RSA-Key hinterlegt werden.

Siehe hierzu: https://wiki.ubuntuusers.de/FUSE/sshfs/


Zur einfacheren Konfiguration wurde in in /etc/rc.local ein eintrag hinzugefügt der /boot/addtoboot.sh ausführt.
Diese initialisiert beim Start den Netzadapter und in falle der Slave-Pis wird ein Ordner mittels SSHFS vom Master gemountet.
Dieser Ordner dient als Sammelstelle für die erzeugten Fotos.

Nach einem Boot sollte mittels der addtoboot.sh das passende Python-Skript gestartet werden. Über eth0 werden befehle und Bilder zwischen Slave und Master Pi getauscht. Mittels Wifi sendet ein Sender an alle Master im Netzwerk. Zu diesem Zweck kann die send.py aus dem Master genutzt werden.


Zusammengefasst:

0. Python 2.7, SSHFS installieren sowie Wlan und RSA-Key einrichten
1. Inhalt des Ordners Master auf die SD-Karte des Pis kopieren der die anderen Pis in einer einheit steuern soll
2. Inhalt des Ordners Slave auf die SD-Karte der Pis kopieren die Fotos erstellen sollen
3. Die IP in addtoboot.sh anpassen - die 3 stelle beschreibt die einheit, die 4 das Element (den Pi)
4. Denn Eintrag "sudo /boot/addtoboot.sh" in /etc/rc.local hinzufügen
5. Darauf achten das homeverzeichnes des Users ein Ordner "files" vorliegt (/home/pi/files)


#Gebrauch

Alle Pis Starten. Die Sleves warten bis ihr Master im Netzwerk ereichbar ist (eth0).
"send.py" starten und einen Wunschnamen eingeben.
Fotos werden in /home/*USER*/files/images/*WUNSCHNAME* gespeichert.
Bilder mittels FTP ziehen.


#Weitere Befehle

Folgende befehle können über send.py als Photo-Name eingegeben werden:

reoot = startet alle Pis neu
poweroff = fährt alle Pis herunter
update = kopiert alle Files aus dem Ordner /boot/update/ nach /home/pi/files/update/. Darauf kopieren alle Slaves diesen in ihr boot-Verzeichnis und starten neu.
stop = beendet das master_listen.py Skript und ermöglicht den direkten Zugrief auf dem master-Pi
