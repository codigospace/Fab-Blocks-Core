import socketio

# Crear una instancia del cliente de Socket.IO
sio = socketio.Client()

# Manejar el evento de conexión
@sio.event
def connect():
    print('Conexión establecida')

# Manejar el evento de desconexión
@sio.event
def disconnect():
    print('Desconectado del servidor')

# Manejar el evento 'execution_output'
@sio.on('execution_output')
def handle_execution_output(data):
    print('Mensaje recibido en execution_output:', data)

# Conectar al servidor
try:
    sio.connect('http://localhost:5000')  # Asegúrate de que esta URL coincida con la de tu servidor
except socketio.exceptions.ConnectionError as e:
    print(f"Error de conexión: {e}")

# Mantener la conexión abierta para recibir mensajes
sio.wait()
