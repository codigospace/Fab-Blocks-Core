import time

# Global variable
i = 0

# Function definition
def setup():
    pass

def loop():
    global i  # Indica que vamos a usar la variable global 'i'
    print(i)
    i += 1
    time.sleep(1)

# Main
setup()

while True:
    loop()
