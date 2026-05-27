import http.server
import socketserver
import webbrowser
import os
from urllib.parse import urlparse, parse_qs

PORT = 8080

# Variable global simulada de modo
modo_web_simulado = False
carro_simulado = "S"
elev_simulado = "S"
giro_simulado = "S"

class MockHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global modo_web_simulado, carro_simulado, elev_simulado, giro_simulado
        parsed_path = urlparse(self.path)
        
        if parsed_path.path.startswith('/cmd'):
            query = parse_qs(parsed_path.query)
            action = query.get('action', [''])[0]
            print(f"\n---> [ESP32 Simulado] Comando recibido: {action}")
            
            if action == 'M':
                modo_web_simulado = not modo_web_simulado
                carro_simulado = "S"
                elev_simulado = "S"
                giro_simulado = "S"
                print(f"      [Modo Simulado] Cambiado a: {'WEB' if modo_web_simulado else 'MANUAL'}")
            elif action == 'F':
                carro_simulado = "F"
            elif action == 'B':
                carro_simulado = "B"
            elif action == 'U':
                elev_simulado = "U"
            elif action == 'D':
                elev_simulado = "D"
            elif action == 'L':
                giro_simulado = "L"
            elif action == 'R':
                giro_simulado = "R"
            elif action == 'S':
                carro_simulado = "S"
                elev_simulado = "S"
                giro_simulado = "S"
                
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"OK")
            
        elif parsed_path.path == '/mode':
            mode_str = "WEB" if modo_web_simulado else "MANUAL"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(mode_str.encode('utf-8'))
            
        elif parsed_path.path == '/status':
            mode_str = "WEB" if modo_web_simulado else "MANUAL"
            status_str = f"{mode_str},{carro_simulado},{elev_simulado},{giro_simulado}"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(status_str.encode('utf-8'))
            
        else:
            # Sirve index.html y otros archivos de la carpeta
            super().do_GET()

# Cambiar directorio dinámicamente para que sirva la carpeta esp32
base_dir = os.path.dirname(os.path.abspath(__file__))
esp32_dir = os.path.join(base_dir, "esp32")
os.chdir(esp32_dir)

Handler = MockHandler
# Permitir reutilizar la dirección para evitar error de puerto ocupado en reinicios rápidos
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Servidor simulado iniciado en http://localhost:{PORT}")
print("Abriendo el navegador...")
webbrowser.open(f"http://localhost:{PORT}")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
