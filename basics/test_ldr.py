from gpiozero import LightSensor
from time import sleep

ldr = LightSensor(7)

while True:
    print(f"LDR value: {ldr.value}")
    sleep(1)