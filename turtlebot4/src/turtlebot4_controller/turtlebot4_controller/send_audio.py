import socket
import pyaudio

# Configuración de la conexión
#HOST = '127.0.0.1'  # Reemplaza con la IP de la máquina receptora
#HOST = '192.168.1.115'
HOST = '192.168.99.199'
PORT = 12345

# Configuración de PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

# Configuración del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Conectado a {HOST}:{PORT}")

# Capturar y enviar audio
try:
    while True:
        data = stream.read(1024)
        client_socket.sendall(data)
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
finally:
    client_socket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
