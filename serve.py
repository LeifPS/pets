#!/usr/bin/env python3
"""
Kleiner lokaler Server für die Kartenpacks-App (index.html).

Warum das nötig ist:
Roblox' Thumbnail-API (thumbnails.roblox.com) blockiert Anfragen, die direkt
aus dem Browser kommen (CORS). Dieser Server liegt "dazwischen": er nimmt die
Anfrage vom Browser entgegen, holt das Bild selbst (serverseitig, ohne
CORS-Einschränkung) und reicht es weiter. Für den Browser sieht es dann so
aus, als käme das Bild von der eigenen Seite - das ist erlaubt.

Start:
    python3 serve.py

Dann im Browser öffnen:
    http://localhost:8000/index.html
"""
import http.server
import urllib.request
import json
import re

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        m = re.match(r"^/thumb/(\d+)$", self.path)
        if m:
            self.serve_thumb(m.group(1))
            return
        super().do_GET()

    def serve_thumb(self, asset_id):
        try:
            api_url = (
                "https://thumbnails.roblox.com/v1/assets"
                f"?assetIds={asset_id}&size=720x720&format=Png&isCircular=false"
            )
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode("utf-8"))

            entries = data.get("data") or []
            image_url = entries[0].get("imageUrl") if entries else None
            if not image_url:
                self.send_error(404, "Roblox lieferte keine imageUrl")
                return

            img_req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=8) as img:
                content = img.read()
                content_type = img.headers.get("Content-Type", "image/png")

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(502, f"Thumbnail-Abruf fehlgeschlagen: {e}")

    def log_message(self, format, *args):
        # ruhiger Log, nur Thumbnail-Anfragen anzeigen
        if "/thumb/" in (args[0] if args else ""):
            super().log_message(format, *args)


if __name__ == "__main__":
    print(f"Server läuft: http://localhost:{PORT}/index.html  (zum Beenden: Strg+C)")
    http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
