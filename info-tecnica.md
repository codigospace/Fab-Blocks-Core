# Fab-Blocks-Core: Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/codigospace/Fab-Blocks-Core.git
cd Fab-Blocks-Core
```

### 2. Crear un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip3 install -r requirements.txt
```

### 4. Instalar la librería localmente
```bash
cd Modular/
pip3 install -e .
```
### Nota: En futuras versiones, la librería 'Modular' será trasladada a un repositorio propio.

### 5. Ejecutar el proyecto Flask
```bash
cd Fab-Blocks-Core
python3 server.py
```

### Notas adicionales:
#### Recuerda activar el entorno virtual cada vez que trabajes con el proyecto usando:
```bash
source venv/bin/activate
```
### Puedes detener el servidor Flask presionando Ctrl+C.
