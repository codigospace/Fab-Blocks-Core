import sys
import platform

# Importar módulos analógicos
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Verificar si se está ejecutando en una Raspberry Pi
if platform.system() == 'Linux' and 'arm' in platform.machine():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
else:
    # Crear una clase simulada para GPIO en entornos no Raspberry Pi
    class FakeGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        IN = 'IN'
        PUD_UP = 'PUD_UP'
        
        @staticmethod
        def setmode(mode):
            pass
        
        @staticmethod
        def setwarnings(flag):
            pass
        
        @staticmethod
        def setup(pin, mode, pull_up_down=None):
            pass
        
        @staticmethod
        def output(pin, state):
            pass
        
        @staticmethod
        def input(pin):
            return 0
        
    GPIO = FakeGPIO()

# Inicialización de I2C y ADS
i2c = busio.I2C(board.SCL, board.SDA)
ads0 = ADS.ADS1115(address=0x48, i2c=i2c)
ads1 = ADS.ADS1115(address=0x49, i2c=i2c)

# Pines y puertos
pines_dos    = [ 4,  27, 6]
pines_cuatro = [17, 22, 5]
port_analog = [ads0, ads0, ads0, ads0, ads1, ads1, ads1, ads1]
pines_analog = [ADS.P0, ADS.P1, ADS.P2, ADS.P3, ADS.P0, ADS.P1, ADS.P2, ADS.P3]

class analogInput:
    def __init__(self, Port):
        self.portAnalogIn = port_analog[Port]
        self.pinAnalogIn = pines_analog[Port]
    def init(self):
        self.channel = AnalogIn(self.portAnalogIn, self.pinAnalogIn)
    def read(self):
        return self.channel.voltage
    def write(self, value):
        pass

class analogOutput:
    def __init__(self, Port):
        self.stateOut = 0
        self.pinDigitalOut = pines_cuatro[Port]
    def init(self):
        GPIO.setup(self.pinDigitalOut, GPIO.OUT)
    def read(self):
        return self.stateOut
    def write(self, state):
        self.stateOut = state
        GPIO.output(self.pinDigitalOut, self.stateOut)

class digitalInput:
    def __init__(self, Port):
        self.pinDigitalIn = pines_cuatro[Port]
    def init(self):
        GPIO.setup(self.pinDigitalIn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.stateInLast = self.read()
    def read(self):
        return GPIO.input(self.pinDigitalIn)
    def write(self, state):
        pass

class digitalOutput:
    def __init__(self, Port):
        self.stateOut = 0
        self.pinDigitalOut = pines_cuatro[Port]
    def init(self):
        GPIO.setup(self.pinDigitalOut, GPIO.OUT)
    def read(self):
        return self.stateOut
    def write(self, state):
        self.stateOut = state
        GPIO.output(self.pinDigitalOut, self.stateOut)
