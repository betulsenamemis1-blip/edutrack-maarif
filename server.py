#!/usr/bin/env python3
"""EduTrack Maarif - Web Sunucusu"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, webbrowser, threading, time

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ogrenci_verisi.json")

def veri_yukle():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Sessiz mod

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
            with open(html_path, "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(veri_yukle()).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/save":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)
            veri_kaydet(data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def acik_tarayici():
    time.sleep(1)
    webbrowser.open("http://localhost:8765")

if __name__ == "__main__":
    print("=" * 50)
    print("  EduTrack Maarif başlatılıyor...")
    print("  http://localhost:8765 adresinde açılacak")
    print("  Kapatmak için: Ctrl+C")
    print("=" * 50)
    threading.Thread(target=acik_tarayici, daemon=True).start()
    server = HTTPServer(("localhost", 8765), Handler)
    server.serve_forever()
