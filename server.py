from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, make_response
import os
import shutil
import tempfile

app = Flask(__name__, static_folder='static')

def execute_python_code():
    return 0

# Ruta para la página principal
@app.route('/')
def index():
    # Asegúrate de que el directorio 'projects' exista
    if not os.path.exists('projects'):
        os.makedirs('projects')
    
    # Obtener la lista de proyectos y ordenarla por fecha de creación
    projects = os.listdir('projects')
    projects = sorted(projects, key=lambda x: os.path.getctime(os.path.join('projects', x)))
    
    return render_template('index.html', projects=projects)

# Ruta para la página de FABBlocks
@app.route('/fabblocks')
def fabblocks():
    return render_template('fabblocks.html')

# Ruta para servir imágenes estáticas
@app.route('/media/<path:filename>')
def serve_image(filename):
    return app.send_static_file(f'media/{filename}')

# Ruta para servir imágenes estáticas
@app.route('/img/blocks/<path:filename>')
def serve_image_lock(filename):
    return app.send_static_file(f'img/blocks/{filename}')

# Ruta para crear un nuevo proyecto
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

# Ruta para eliminar un proyecto
@app.route('/delete_project/<project_name>', methods=['POST'])
def delete_project(project_name):
    path = os.path.join('projects', project_name)
    if os.path.exists(path):
        shutil.rmtree(path)
    return redirect(url_for('index'))

# Ruta para editar un proyecto
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
        # Si existe un archivo .py, abre y lee su contenido
        with open(python_file_path, "r") as python_file:
            python_content = python_file.read()
        # Renderiza la plantilla 'editor_python.html' con el contenido del archivo .py
        return render_template('editor_python.html', project=project_name, python_content=python_content)
    else:
        # Si no existe un archivo .py, lee el contenido del archivo .fab
        with open(fab_file_path, "r") as fab_file:
            fab_content = fab_file.read()
        # Renderiza la plantilla 'project_content.html' con el contenido del archivo .fab
        return render_template('project_content.html', project=project_name, fab_content=fab_content)


@app.route('/save_project', methods=['POST'])
def save_project():
    project_name = request.form['project_name']
    xml_content = request.form['xml_content']
    
    # Guardar el XML en un archivo
    fab_file_path = os.path.join('projects', str(project_name), f"{project_name}.fab")
    with open(fab_file_path, "w") as fab_file:
        fab_file.write(xml_content)
    
    return jsonify({"status": "success", "message": "Proyecto guardado exitosamente."})

@app.route('/edit_code', methods=['POST'])
def edit_code():
    # Obtener el código Python enviado desde el cliente
    code_with_newlines = request.form['code']
    
    # Reemplazar los caracteres especiales por saltos de línea
    code_python = code_with_newlines.replace('\\n', '\n')
    
    # Nombre del proyecto
    project_name = request.form['project_name']
    
    # Ruta donde se guardará el archivo .py
    python_file_path = os.path.join('projects', project_name, f"{project_name}.py")

    fab_file_path = os.path.join('projects', project_name, f"{project_name}.fab")
    if os.path.exists(fab_file_path):
        os.remove(fab_file_path)
    
    # Guardar el código Python en el archivo .py
    with open(python_file_path, "w") as python_file:
        python_file.write(code_python)
    
    # Renderizar la plantilla 'editor_python.html' y pasar el código Python si es necesario
    return render_template('editor_python.html', code_python=code_python)

@app.route('/save_python', methods=['POST'])
def save_python():
    code_with_newlines = request.form['python_content']
    code_python = code_with_newlines.replace('\\n', '\n')
    project_name = request.form['project_name']
    python_file_path = os.path.join('projects', project_name, f"{project_name}.py")
    
    # Guardar el código Python en el archivo .py
    with open(python_file_path, "w") as python_file:
        python_file.write(code_python)
    
    return jsonify({"status": "success", "message": "Proyecto actualizado exitosamente."})

@app.route('/import_project', methods=['POST'])
def import_project():
    # Verificar si se ha proporcionado un archivo
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No se ha proporcionado ningún archivo."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No se ha seleccionado ningún archivo."}), 400

    # Guardar el archivo temporalmente
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    # Verificar la extensión del archivo y proceder en consecuencia
    file_extension = os.path.splitext(file.filename)[1].lower()
    project_name = os.path.splitext(file.filename)[0]

    if file_extension == '.fab':
        # Crear un nuevo directorio para el proyecto
        project_path = os.path.join('projects', project_name)
        os.makedirs(project_path)

        # Mover el archivo .fab al directorio del proyecto
        shutil.move(file_path, os.path.join(project_path, f"{project_name}.fab"))

        return jsonify({"status": "success", "message": "Proyecto importado exitosamente."}), 201

    elif file_extension == '.py':
        # Crear un nuevo directorio para el proyecto
        project_path = os.path.join('projects', project_name)
        os.makedirs(project_path)

        # Mover el archivo .py al directorio del proyecto
        shutil.move(file_path, os.path.join(project_path, f"{project_name}.py"))

        return jsonify({"status": "success", "message": "Proyecto importado exitosamente."}), 201

    else:
        # Eliminar el archivo temporal
        os.remove(file_path)
        return jsonify({"status": "error", "message": "Formato de archivo no compatible."}), 400

@app.route('/export_project/<project_name>', methods=['GET'])
def export_project(project_name):
    # Ruta donde se encuentra el archivo a exportar
    project_path = os.path.join('projects', project_name)
    
    # Verificar si hay un archivo .fab o .py en la carpeta del proyecto
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
