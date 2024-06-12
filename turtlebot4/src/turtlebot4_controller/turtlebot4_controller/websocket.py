from flask_socketio import SocketIO
import time

def emit_data_update():
    # Simula la obtención de nuevos valores de datos
    client_ip = "192.168.1.10"
    client_port = 8000
    client_id = 123
    client_os = "Windows 10"
    topic = "Datos del sensor"
    param_x = 10.5
    param_y = 22.3
    param_z = 3.14

    # Emite un evento con los nuevos valores de datos
    SocketIO.emit('data_update', {
        'client_ip': client_ip,
        'client_port': client_port,
        'client_id': client_id,
        'client_os': client_os,
        'topic': topic,
        'param_x': param_x,
        'param_y': param_y,
        'param_z': param_z
    })

@SocketIO.on('connect', namespace='/test')  # Listen for 'connect' event
def handle_connect():
    print('Client connected')

@SocketIO.on('disconnect')  # Listen for 'disconnect' event
def handle_disconnect():
    print('Client disconnected')

@SocketIO.on('timer')  # Listen for 'timer' event
def handle_timer():
    emit_data_update()
