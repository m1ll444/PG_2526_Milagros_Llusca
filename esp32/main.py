import uasyncio as asyncio
import machine
import os

# Configuración de UART (Pines TX=17, RX=16 - usando solo TX)
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

def leer_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        print("Error leyendo index.html:", e)
        return "<html><body><h1>Error: No se encontro index.html</h1></body></html>"

html_content = leer_html()

async def handle_client(reader, writer):
    try:
        request_line = await reader.readline()
        if not request_line:
            return
            
        request_line = request_line.decode('utf-8').strip()
        print("Petición recibida:", request_line)
        
        # Leer cabeceras restantes
        while True:
            line = await reader.readline()
            if not line or line == b'\r\n':
                break
        
        # Analizar ruta y parámetros
        parts = request_line.split()
        if len(parts) > 1:
            method = parts[0]
            path = parts[1]
            
            # Servir página principal
            if path == '/' or path == '/index.html':
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_content
                await writer.awrite(response)
                
            # Endpoint para comandos (/cmd?action=F)
            elif path.startswith('/cmd'):
                cmd_param = ''
                if '?' in path:
                    query = path.split('?')[1]
                    params = query.split('&')
                    for p in params:
                        if p.startswith('action='):
                            cmd_param = p.split('=')[1]
                
                if cmd_param:
                    # Enviar el comando al Arduino vía UART
                    print(f"Enviando comando UART: {cmd_param}")
                    uart.write(cmd_param)
                    
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
                else:
                    response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing action"
                    
                await writer.awrite(response)
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
                await writer.awrite(response)
    
    except Exception as e:
        print("Error manejando cliente:", e)
    finally:
        await writer.aclose()

async def main():
    print("Iniciando servidor web...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("Servidor web corriendo en el puerto 80.")
    
    while True:
        await asyncio.sleep(1)

# Iniciar bucle de eventos
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor detenido.")
