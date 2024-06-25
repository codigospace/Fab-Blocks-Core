import time

# Global variables
int i=0;

# Function definition

def setup():



    Serial.begin(115200);

def loop():
    Serial.println(i);
    i=i + 1;
    time.sleep(1000)

# Main
setup()

while True:
    loop()
