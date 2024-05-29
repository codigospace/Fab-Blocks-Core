import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P3)
try:
	while 1:
		print("Analog 0 Value: ", channel0.value, "Voltage 0: ", channel0.voltage)
		print("Analog 1 Value: ", channel1.value, "Voltage 1: ", channel1.voltage)
		time.sleep(0.2)
except KeyboardInterrupt:
	GPIO.cleanup()
