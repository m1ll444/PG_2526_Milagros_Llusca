import http.server
import socketserver
import webbrowser
import os
from urllib.parse import urlparse, parse_qs

PORT = 8080

class MockHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/cmd'):
            query = parse_qs(parsed_path.query)
            action = query.get('action', [''])[0]
            print(f"\n---> [ESP32 Simulado] Comando recibido: {action}")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            # Sirve index.html y otros archivos de la carpeta
            super().do_GET()

# Cambiar directorio para que sirva la carpeta esp32
os.chdir(r"c:\Users\Mili\Documents\Proyecto de Grado\PG_2526_Milagros_Llusca\esp32")

Handler = MockHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Servidor simulado iniciado en http://localhost:{PORT}")
print("Abriendo el navegador...")
webbrowser.open(f"http://localhost:{PORT}")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
