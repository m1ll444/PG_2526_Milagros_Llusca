import uasyncio as asyncio
import machine

# Configuración de UART (Pines TX=17, RX=16). Arduino TX va a ESP32 RX (16).
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

logs = ["[SISTEMA] Monitor de depuración iniciado."]
MAX_LOGS = 50

def add_log(msg):
    global logs
    logs.append(msg)
    if len(logs) > MAX_LOGS:
        logs.pop(0)

async def leer_uart_logs():
    """Tarea asíncrona para leer logs del Arduino."""
    uart_buffer = b""
    while True:
        if uart.any():
            data = uart.read(uart.any())
            if data:
                uart_buffer += data
                while b'\n' in uart_buffer:
                    line_bytes, uart_buffer = uart_buffer.split(b'\n', 1)
                    try:
                        line = line_bytes.decode('utf-8', 'ignore').strip()
                        if line:
                            add_log(line)
                            print(line) # También imprime en consola REPL
                    except Exception as e:
                        print("Error decodificando log:", e)
        await asyncio.sleep_ms(50)

async def handle_client(reader, writer):
    try:
        request_line = await reader.readline()
        if not request_line:
            return
            
        request_line = request_line.decode('utf-8').strip()
        parts = request_line.split()
        if len(parts) > 1:
            path = parts[1]
            
            # Leer cabeceras restantes
            while True:
                line = await reader.readline()
                if not line or line == b'\r\n':
                    break
            
            # Servir página de logs
            if path == '/' or path == '/index.html':
                # Renderizar logs (de más antiguo a más nuevo)
                contenido_logs = "\n".join(logs)
                html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="2">
<title>Logs - Grua Torre</title>
<style>
body { background-color: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; margin: 0; }
h1 { border-bottom: 1px solid #00ff41; padding-bottom: 5px; font-size: 1.1rem; margin-top: 0; }
pre { white-space: pre-wrap; word-wrap: break-word; line-height: 1.3; font-size: 0.9rem; }
</style>
</head>
<body>
<h1>📟 GRUA TORRE - TERMINAL DE DEPURACION</h1>
<pre>""" + contenido_logs + """</pre>
</body>
</html>"""
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + html
                await writer.awrite(response)
            else:
                response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
                await writer.awrite(response)
    except Exception as e:
        print("Error en conexion:", e)
    finally:
        await writer.aclose()

async def main():
    print("Iniciando servidor de logs...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    
    # Iniciar lectura UART
    asyncio.create_task(leer_uart_logs())
    print("Lectura de logs por UART activa.")
    
    while True:
        await asyncio.sleep(1)

# Iniciar bucle de eventos
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor detenido.")
