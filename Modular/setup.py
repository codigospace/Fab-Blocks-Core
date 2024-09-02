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
)

setup(
    name='pymodular',
    version='0.1',
    packages=find_packages(),
    description='PyModular',
    author='Codigo',
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