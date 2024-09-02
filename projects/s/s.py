import pymodular
import time
led = pymodular.digitalOutput(1)
try:
	led.init()
	while 1:
		led.write(1)
		time.sleep(1)
		led.write(0)
		time.sleep(1)
except KeyboardInterrupt:
	print("d")
