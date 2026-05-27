import uasyncio as asyncio
import machine
import os

# Configuración de UART (Pines TX=17, RX=16)
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

# Variable global de modo de control
current_mode = 'MANUAL'
current_telemetry = 'MANUAL,S,S,S'

def leer_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        print("Error leyendo index.html:", e)
        return "<html><body><h1>Error: No se encontro index.html</h1></body></html>"

html_content = leer_html()

async def leer_uart_modo():
    """Tarea asíncrona para leer telemetría desde Arduino."""
    global current_mode, current_telemetry
    uart_buffer = ""
    while True:
        if uart.any():
            data = uart.read(uart.any())
            if data:
                try:
                    text = data.decode('utf-8', 'ignore')
                    uart_buffer += text
                    while '\n' in uart_buffer:
                        line, uart_buffer = uart_buffer.split('\n', 1)
                        line = line.strip()
                        if line.startswith('S:'):
                            parts = line[2:].split(',')
                            if len(parts) == 4:
                                mode_char, carro, elev, giro = parts
                                current_mode = 'WEB' if mode_char == 'W' else 'MANUAL'
                                current_telemetry = f"{current_mode},{carro},{elev},{giro}"
                                print(f"Telemetria: {current_telemetry}")
                except Exception as e:
                    print("Error leyendo UART:", e)
        await asyncio.sleep_ms(50)

async def handle_client(reader, writer):
    global current_mode
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
                    
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\nOK"
                else:
                    response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing action"
                    
                await writer.awrite(response)
            
            # Endpoint para consultar modo actual
            elif path == '/mode':
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + current_mode
                await writer.awrite(response)
                
            # Endpoint para consultar telemetría actual
            elif path == '/status':
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + current_telemetry
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
    
    # Iniciar tarea de lectura UART para modo
    asyncio.create_task(leer_uart_modo())
    print("Lectura UART de modo activa.")
    
    while True:
        await asyncio.sleep(1)

# Iniciar bucle de eventos
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor detenido.")
