import time
import random

def setup():
  pass

def loop():
    print(f"Potenciometro:{random.randint(2,3)}")
    time.sleep(0.2)

# Main
setup()

while True:
    loop()