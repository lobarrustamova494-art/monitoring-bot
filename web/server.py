"""Simple web server for landing page"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)

if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("localhost", port), MyHandler)
    print(f"🌐 Landing page ishga tushdi!")
    print(f"📍 Manzil: http://localhost:{port}")
    print(f"⏹️  To'xtatish uchun Ctrl+C bosing\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server to'xtatildi")
        server.shutdown()
