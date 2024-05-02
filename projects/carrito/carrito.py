import Modular

# Global variables
name = analogInput(1);

# Function definition

def setup():
      name.init();

def loop():
    name.write(HIGH);

# Main
setup()

while True:
    loop()
