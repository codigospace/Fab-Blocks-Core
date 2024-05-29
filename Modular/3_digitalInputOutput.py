import pymodular
import time
led = pymodular.digitalOutput(1)
but = pymodular.digitalInput(0)
try:
	led.init()
	but.init()
	while 1:
		if but.read():
			led.write(1)
		else:
			led.write(0)
except KeyboardInterrupt:
	print("ga")
