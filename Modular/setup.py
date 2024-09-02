from setuptools import setup, find_packages
import platform

install_requires = [
    'adafruit-circuitpython-ads1x15',
]

# Añadir RPi.GPIO solo si estamos en una máquina Linux con arquitectura ARM
if platform.system() == 'Linux' and 'arm' in platform.machine():
    install_requires.append('RPi.GPIO')

setup(
    name='pymodular',
    version='0.1',
    description='PyModular',
    author='Codigo',
    py_modules=['pymodular'],  # Si pymodular2.py es un módulo independiente
    packages=find_packages(),  # Encuentra y lista automáticamente todos los paquetes
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=install_requires,
)
