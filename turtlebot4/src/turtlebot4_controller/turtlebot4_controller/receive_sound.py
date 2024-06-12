import socket
import pyaudio
import time

# Configuración de la conexión
HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 12345

# Configuración de PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True)

# Configuración del socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Esperando conexión en {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"Conectado por {addr}")

# Recibir y reproducir audio
try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        stream.write(data)
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
finally:
    conn.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
