# Vulnscanner Automatisierung
Automatisierung von Amass + Nmap + Nikto.

# Setup
Du solltest Amass, Nmap und Nikto installiert haben. Am besten direkt in
Kali Linux starten!

# Nutzung
``` bash
python3 scanner.py
```
Du wirst interaktiv nach dem Domainnamen gefragt.
Gibt den Domainnamen ohne http// oder www. ein
Zum Beispiel: scanme.nmap.org

# Auswertung
Suche in nmap.txt nach "CVE" Das zeigt die gefundenen Sicherheitslücken an.
Die Informationen basieren auf den erkannten Versionsnummern und können deshalb 
auch falsch sein, wenn die falsche Versionsnummer ausgegeben oder erkannt wird.
