from setuptools import setup, find_packages
import platform

install_requires = [
    'adafruit-circuitpython-ads1x15',
]

if platform.system() == 'Linux' and 'arm' in platform.machine():
    install_requires.append('RPi.GPIO')

setup(
    name='pymodular',
    version='0.1',
    py_modules=['pymodular'],
    install_requires=install_requires,
)
