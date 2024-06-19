import pymodular

import time

# Global variables
adc = pymodular.analogInput(0)

# Function definition

def setup():
      adc.init()

def loop():
    print(adc.read())
    time.sleep(1)

# Main
setup()

while True:
    loop()
