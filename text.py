from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('test.html')

def run_python_code(code):
    try:
        exec(code, globals())
    except Exception as e:
        return str(e)

@socketio.on('execute_code')
def execute_code(code):
    output = run_python_code(code)
    socketio.emit('output', output)

if __name__ == '__main__':
    socketio.run(app)
