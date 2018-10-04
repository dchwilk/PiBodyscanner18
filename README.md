# Raspberry Pi 3D Bodyscanner

Die Raspberry Pi Kamera gehört zu den günstigsten Digitalkameras. Nahezu konkurenzlos wird diese, wenn der Anwendungskontext Anforderungen stellt, die über das bloße Fotografieren hinaus gehen. Das Ziel dieses Projektes war die Realisierung eines 3D-Bodyscanners, welcher in seiner Größe problemlos erweiterbar sein sollte.

Dieses Projekt ist dabei teilweise inspiriert von folgendem Projekt:
https://www.instructables.com/id/Multiple-Raspberry-PI-3D-Scanner/

Dabei erstellen die Pis nur die Bilder welche seperat mittels SFM verarbeitet werden.

Anders als vergleichbare Projekte abeitet dieses Projekt mit einer Hierarchisierung. Ein Master-Pi steuert n-viele Slave-Pis. So können getrennte Einheiten aufgebaut werden und ein Mesh von Scannern kann gemeinschaftlich Fotos erstellen. Jede Einheit lässt sich frei positionieren.


#Installation

Für dieses Projekt wurde Raspian verwendet. Allerdings ist grundsätzlich jedes Raspbery-OS denkbar solange Python 2.7 und die Pi Kamera unterstützt werden.
Des weiteren muss SSHFS installiert sein und auf jedem Pi der passende RSA-Key hinterlegt werden.

Siehe hierzu: https://wiki.ubuntuusers.de/FUSE/sshfs/


Zur einfacheren Konfiguration wurde in in /etc/rc.local ein Eintrag hinzugefügt, der /boot/addtoboot.sh ausführt. Diese initialisiert beim Start den Netzadapter und im Falle der Slave-Pis wird ein Ordner mittels SSHFS vom Master gemountet. Dieser Ordner dient als Sammelstelle für die erzeugten Fotos.

Nach einem Boot sollte mittels der addtoboot.sh das passende Python-Skript gestartet werden. Über eth0 werden befehle und Bilder zwischen Slave und Master Pi getauscht. Mittels Wifi sendet ein Sender an alle Master im Netzwerk. Zu diesem Zweck kann die send.py aus dem Master genutzt werden.


Zusammengefasst:

0. Python 2.7, SSHFS installieren sowie Wlan und RSA-Key einrichten
1. Inhalt des Ordners Master auf die SD-Karte jenes Pis kopieren, der die anderen Pis in einer Einheit steuern soll
2. Inhalt des Ordners Slave auf die SD-Karte jener Pis kopieren, die die Fotos erstellen sollen
3. Die IP in addtoboot.sh anpassen - die 3. Stelle beschreibt die einheit, die 4. das Element (den Pi)
4. Den Eintrag "sudo /boot/addtoboot.sh" in /etc/rc.local hinzufügen
5. Darauf achten, dass im Homeverzeichnes des Users ein Ordner "files" vorliegt (/home/pi/files)


#Gebrauch

Alle Pis starten. Die Slaves warten bis ihr Master im Netzwerk ereichbar ist (eth0).
"send.py" starten und einen Wunschnamen eingeben.
Fotos werden in /home/*USER*/files/images/*WUNSCHNAME* gespeichert.
Bilder mittels FTP herunterladen.


#Weitere Befehle

Folgende Befehle können über send.py als Foto-Name eingegeben werden:

reboot = Startet alle Pis neu
poweroff = Fährt alle Pis herunter
update = Kopiert alle Files aus dem Ordner /boot/update/ nach /home/pi/files/update/. Daraufhin kopieren alle Slaves diesen in ihr boot-Verzeichnis und starten neu.
stop = Beendet das master_listen.py Skript und ermöglicht den direkten Zugriff auf den Master-Pi
