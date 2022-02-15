# climate.local
here you have the worlds first hacked fridge to grow any kind of organism.



so kriegst du den Kühlschrank zum Laufen:

1) Kühlschrank an einem nicht zu heißen Ort mit ausreichend
Kühlluftzufuhr für den Kompressor aufstellen

2) RasPi und Aggregatstecker in die Steckdose stecken
(5V-Netzteil=RasPi, SchuKo Stecker=Versorgungsspannung der
Box/Aggregate; der RasPi läuft auch ohne Strom für die Aggregate)

3) Warten bis die Relais Lichter angehen. Dann läuft das Programm. Der
Kühlschrank verbindet sich automatisch mit dem MachBar Netz (Einstellung
siehe etc/wpa_supplicant/wpa_supplicant.conf auf dem RasPi)

4) An einem Rechner, der im selben Wlan hängt, die Konsole aufmachen und
mittels "ping climate.local" den Kühlschrank anpingen. Dabei siehst du
die vom Router zugewiesene IP Adresse (192.168.???.???)

5) Web Browser an einem Gerät, das ebenfalls mit dem selben Wlan
verbunden ist, den Webbrowser öffnen und die IP:8080 aufrufen, z.B.
192.168.1.212:8080

Der Kühlschrank ist intern auf 5-40°C begrenzt. Per Default sind 20°C
vorgegeben. Die Genauigkeit variiert, am besten triffst du deine
Zieltemperatur wenn du im Fall
Umgebungstemperatur > Zieltemperatur: Zieltemperatur - 1°C einstellst
und im Fall
Umgebungstemperatur < Zieltemperatur: Zieltemperatur + 1°C einstellst.

Bei >42°C schaltet der Kühlschrank für 15min. ab. Ebenso wenn der
Kühlkompressor länger als 45min. am Stück in Betrieb war (z.B. wenn du
von 40°C auf 5°C abkühlen willst oder die Tür offen geblieben ist u.ä.)

Das Updaten der Daten per Webinterface kann bis zu 1min. dauern. Zu
häufiges Neuladen hilft da nichts, lieber ein wenig warten und dann
nochmal auf den Button klicken.

Logdaten ind damit Infos über die internen Zustände kannst du direkt auf
dem RasPi einsehen. Entweder in der log.txt oder in den alten Logs unter
~/oldlogs/.

Der Zugang zum Pi ist: ssh pi@climate.local
Passwort:XXX

![BMBF_gefördert vom_deutsch](https://user-images.githubusercontent.com/29493121/154106082-bd94244b-91b7-4321-b3c2-514690e07f42.jpg)

Die Verantwortung dieser Veröffentlichung für den Inhalt dieser Veröffentlichung liegt beim Autor.
