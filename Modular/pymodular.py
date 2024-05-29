#digital
import RPi.GPIO as GPIO
#analog
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#digital
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#analog
i2c = busio.I2C(board.SCL, board.SDA)
ads0 = ADS.ADS1115(address=0x48,i2c=i2c)
ads1 = ADS.ADS1115(address=0x49,i2c=i2c)
#Modular
pines_dos    = [ 1,  2]
pines_cuatro = [17, 23]
port_analog  = [  ads0,   ads0,   ads0,   ads0,   ads1,   ads1,   ads1,   ads1]
pines_analog = [ADS.P0, ADS.P1, ADS.P2, ADS.P3, ADS.P0, ADS.P1, ADS.P2, ADS.P3]

class analogInput:
	def __init__(self, Port):
		selfe.portAnalogIn = port_analog[Port]
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
		self.stateOut=state
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
		self.stateOut=state
		GPIO.output(self.pinDigitalOut, self.stateOut)
