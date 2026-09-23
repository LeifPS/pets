# Pets Go – Kartenpacks

Eine lokale Sammelkarten-App für Pets Go (Roblox), inklusive gewichteter
Zufallsziehung nach echtem Spielwert ("difficulty"), Sammlung, PDF-Export
im Pokémon-Kartenformat und optionalem Bild-Proxy für echte Roblox-Thumbnails.

## Nutzung

**Ohne echte Bilder (einfach):**
Öffne `index.html` direkt im Browser (Doppelklick).

**Mit echten Roblox-Bildern:**
```bash
python3 serve.py
```
Dann im Browser öffnen: http://localhost:8000/index.html

Der kleine Proxy-Server umgeht die Browser-CORS-Sperre von Robloxs
Thumbnail-API, indem er die Bild-Anfragen serverseitig stellt.

## Funktionen

- Gewichtete Zufallsziehung nach echtem Spielwert (Stärke/"difficulty")
- 11 Stärke-Ränge (Gewöhnlich bis Geheim) plus eigene Stufen für Riesig/Titanisch
- „Quelle"-Auswahl: normale Pets oder ein bestimmtes Event/Set gezielt ziehen
- Deutsche Pet-Namen (automatisch übersetzt, Komposita mit korrektem Genus)
- Sammlung mit Fortschrittsanzeige, Filtern nach Set/Rang/besessen
- Eigene Bilder pro Pet hochladbar (lokal gespeichert)
- PDF-Export im echten Pokémon-Kartenformat (63,5×88,9 mm, 9 pro A4-Seite)
  inkl. eingebetteter Schriftart und abgerundeten Ecken
- Alles läuft lokal im Browser, keine Cloud, keine Accounts
