from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, make_response
import os
import shutil
import tempfile
import ast
import json
from datetime import datetime
import subprocess
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()
import time
import sys

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

def save_data(data):
    filename = 'data.json'
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    existing_data.append(data)
    
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)
        
def execute_python_code():
    return 0

@app.route('/')
def index():
    if not os.path.exists('projects'):
        os.makedirs('projects')
    
    projects = os.listdir('projects')
    projects = sorted(projects, key=lambda x: os.path.getctime(os.path.join('projects', x)))
    
    return render_template('index.html', projects=projects)

@app.route('/fabblocks')
def fabblocks():
    return render_template('fabblocks.html')

@app.route('/media/<path:filename>')
def serve_image(filename):
    return app.send_static_file(f'media/{filename}')

@app.route('/img/blocks/<path:filename>')
def serve_image_lock(filename):
    return app.send_static_file(f'img/blocks/{filename}')

@app.route('/create_project/<project_name>', methods=['POST'])
def create_project(project_name):
    path = os.path.join('projects', project_name)
    if not os.path.exists(path):
        os.makedirs(path)
        with open(os.path.join(path, f"{project_name}.fab"), 'w') as f:
            f.write('<xml id="startBlocks" style="display: none"><block type="controls_setupLoop" deletable="false"></block></xml>')
        return jsonify({"status": "success", "message": "Proyecto creado exitosamente."}), 201
    else:
        return jsonify({"status": "error", "message": "Proyecto ya existe."}), 400

@app.route('/delete_project/<project_name>', methods=['POST'])
def delete_project(project_name):
    path = os.path.join('projects', project_name)
    if os.path.exists(path):
        shutil.rmtree(path)
    return redirect(url_for('index'))

@app.route('/edit_project/<project_name>', methods=['GET', 'POST'])
def edit_project(project_name):
    path = os.path.join('projects', project_name)
    if request.method == 'POST':
        new_project_name = request.form['new_project_name']
        new_path = os.path.join('projects', new_project_name)
        if os.path.exists(path):
            os.rename(path, new_path)
        return redirect(url_for('index'))
    else:
        return render_template('edit_project.html', project_name=project_name)

@app.route('/project/<project_name>', methods=['GET'])
def project_content(project_name):
    fab_file_path = os.path.join('projects', str(project_name), f"{project_name}.fab")
    python_file_path = os.path.join('projects', str(project_name), f"{project_name}.py")

    if os.path.exists(python_file_path):
        with open(python_file_path, "r") as python_file:
            python_content = python_file.read()
        return render_template('editor_python.html', project=project_name, python_content=python_content)
    else:
        if os.path.exists(fab_file_path):
            with open(fab_file_path, "r") as fab_file:
                fab_content = fab_file.read()
            return render_template('project_content.html', project=project_name, fab_content=fab_content)
        else:
            return "No se encontró ningún archivo para mostrar", 404

@app.route('/projectGraphic/<project_name>', methods=['GET'])
def project_content_graphic(project_name):
    fab_file_path = os.path.join('projects', str(project_name), f"{project_name}.fab")

    if os.path.exists(fab_file_path):
        with open(fab_file_path, "r") as fab_file:
            fab_content = fab_file.read()
        return render_template('project_content.html', project=project_name, fab_content=fab_content)
    else:
        return "No se encontró ningún archivo para mostrar", 404

@app.route('/projectGraphicStatus/<project_name>', methods=['GET'])
def project_content_graphic_status(project_name):
    fab_file_path = os.path.join('projects', str(project_name), f"{project_name}.fab")

    if os.path.exists(fab_file_path):
        return jsonify({"status":"success","message":"Proyecto existente"})
    else:
        return jsonify({"status":"error","message":"Proyecto no encontrado"})

@app.route('/save_project', methods=['POST'])
def save_project():
    project_name = request.form['project_name']
    xml_content = request.form['xml_content']
    
    fab_file_path = os.path.join('projects', str(project_name), f"{project_name}.fab")
    with open(fab_file_path, "w") as fab_file:
        fab_file.write(xml_content)
    
    return jsonify({"status": "success", "message": "Proyecto guardado exitosamente."})

@app.route('/edit_code', methods=['POST'])
def edit_code():
    code_with_newlines = request.form['code']
    
    code_python = code_with_newlines.replace('\\n', '\n')
    
    project_name = request.form['project_name']
    
    python_file_path = os.path.join('projects', project_name, f"{project_name}.py")
    
    with open(python_file_path, "w") as python_file:
        python_file.write(code_python)
    
    return render_template('editor_python.html', code_python=code_python)

@app.route('/save_python', methods=['POST'])
def save_python():
    code_with_newlines = request.form['python_content']
    code_python = code_with_newlines.replace('\\n', '\n')
    project_name = request.form['project_name']
    python_file_path = os.path.join('projects', project_name, f"{project_name}.py")
    
    with open(python_file_path, "w") as python_file:
        python_file.write(code_python)
    
    return jsonify({"status": "success", "message": "Proyecto actualizado exitosamente."})

@app.route('/import_project', methods=['POST'])
def import_project():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No se ha proporcionado ningún archivo."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No se ha seleccionado ningún archivo."}), 400

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    file_extension = os.path.splitext(file.filename)[1].lower()
    project_name = os.path.splitext(file.filename)[0]

    if file_extension == '.fab':
        project_path = os.path.join('projects', project_name)
        os.makedirs(project_path)

        shutil.move(file_path, os.path.join(project_path, f"{project_name}.fab"))

        return jsonify({"status": "success", "message": "Proyecto importado exitosamente."}), 201

    elif file_extension == '.py':
        project_path = os.path.join('projects', project_name)
        os.makedirs(project_path)

        shutil.move(file_path, os.path.join(project_path, f"{project_name}.py"))

        return jsonify({"status": "success", "message": "Proyecto importado exitosamente."}), 201

    else:
        os.remove(file_path)
        return jsonify({"status": "error", "message": "Formato de archivo no compatible."}), 400

@app.route('/export_project/<project_name>', methods=['GET'])
def export_project(project_name):
    project_path = os.path.join('projects', project_name)
    
    fab_file_path = os.path.join(project_path, f"{project_name}.fab")
    py_file_path = os.path.join(project_path, f"{project_name}.py")

    if os.path.isfile(fab_file_path):
        response = make_response(send_from_directory(project_path, f"{project_name}.fab"))
        response.headers["Content-Disposition"] = f"attachment; filename={project_name}.fab"
        return response
    elif os.path.isfile(py_file_path):
        response = make_response(send_from_directory(project_path, f"{project_name}.py"))
        response.headers["Content-Disposition"] = f"attachment; filename={project_name}.py"
        return response
    else:
        return "No se encontró ningún archivo para exportar", 404

@app.route('/verify_code', methods=['POST'])
def verify_code():
    codigo = request.form['codigo']
    try:
        codigo_clean = eval(f'f"""{codigo}"""')
        print(codigo_clean)
        ast.parse(codigo_clean)
        return jsonify({"status": "success", "message": "El código es válido."})
    except SyntaxError:
        return jsonify({"status": "error", "message": "Error de sintaxis"})
    
@app.route('/encuesta')
def review():
    return render_template('review.html')

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    tools_opinion = request.form['tools_opinion']
    session_opinion = request.form['session_opinion']
    preferences = request.form['preferences']
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        'timestamp': current_datetime,
        'tools_opinion': tools_opinion,
        'session_opinion': session_opinion,
        'preferences': preferences
    }
    
    save_data(data)
    return redirect(url_for('index'))

execution_active = True
current_process = None

@socketio.on('cancel_execution_signal')
def cancel_execution_signal():
    global execution_active
    execution_active = False

@socketio.on('execute_code')
def execute_code(data):
    global current_process
    project_name = data['project_name']

    global execution_active
    execution_active = True
    python_file_path = os.path.join('projects', project_name, f"{project_name}.py")

    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'  # Desactivar el almacenamiento en búfer de stdout y stderr
    env['PYTHONIOENCODING'] = 'utf-8'  # Asegurar la codificación utf-8 para la salida

    # Terminar el subproceso actual si está en ejecución
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()

    # Obtener la ruta del intérprete de Python del entorno virtual
    python_executable = sys.executable

    # Iniciar un nuevo subproceso usando el intérprete del entorno virtual
    current_process = subprocess.Popen(
        [python_executable, '-u', python_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    # Leer las líneas de salida y enviarlas
    try:
        while execution_active and not current_process.poll():
            output = current_process.stdout.readline()
            if output:
                socketio.emit('execution_output', {'output': output.strip()})
                socketio.sleep(0)
            else:
                break
    finally:
        if not execution_active:
            current_process.kill()
        current_process.wait()
        socketio.emit('execution_complete', {'result': current_process.returncode})

@app.route('/documentacion/<path:filename>')
def serve_documentation(filename):
    documentation_path = os.path.join('documentation', filename)
    if os.path.exists(documentation_path):
        return send_from_directory(directory='documentation', path=filename)
    else:
        return jsonify({"status": "error", "message": "Archivo no encontrado."}), 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
