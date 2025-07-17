# Import modules
from gpiozero import LightSensor
import gpiod
import time

# Stepper motor ULN2003 IN1-IN4
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

ControlPin = [IN1, IN2, IN3, IN4]

# Stepper motor steps for opening shield
steps_open = 128

# Create a GPIO chip and get the lines
chip = gpiod.Chip('gpiochip4')
lines = [chip.get_line(pin) for pin in ControlPin]

# Configure the lines as outputs
for line in lines:
   line.request('stepper_motor', gpiod.LINE_REQ_DIR_OUT, 0)

# Define the segment pattern
seg_right = [
   [1, 0, 0, 0],
   [1, 1, 0, 0],
   [0, 1, 0, 0],
   [0, 1, 1, 0],
   [0, 0, 1, 0],
   [0, 0, 1, 1],
   [0, 0, 0, 1],
   [1, 0, 0, 1]
]

seg_left = [
   [0, 0, 0, 1],
   [0, 0, 1, 1],
   [0, 0, 1, 0],
   [0, 1, 1, 0],
   [0, 1, 0, 0],
   [1, 1, 0, 0],
   [1, 0, 0, 0],
   [1, 0, 0, 1]
]

delay = 0.002 # set delay

# Streaks
fog_streak = 0
sun_streak = 0

# Light Sensor
ldr = LightSensor(4)

def step_motor_clockwise(steps):
    """Move motor by number of steps clockwise"""
    global lines
    global delay
    global seg_right
    for i in range(steps):
        for halfstep in range(8):
            for pin in range(4):
                lines[pin].set_value(seg_right[halfstep][pin])
            time.sleep(delay)

def step_motor_anticlockwise(steps):
    """Move motor by number of steps antoclockwise"""
    global seg_left
    global lines
    global delay
    for i in range(steps):
        for halfstep in range(8):
            for pin in range(4):
                lines[pin].set_value(seg_left[halfstep][pin])
            time.sleep(delay)

def cleanup_motor():
    """Turn off all motor coils"""
    global chip
    global lines
    for line in lines:
        line.release()
    chip.close()

def fog_or_sun(ldr_value):
    """Returns a string for the type of weather(fog, sun)"""
    print(ldr_value)
    if ldr_value < 4:
        return "sun"
    else:
        return "fog"

def motor_on_weather(ldr, fog_streak, sun_streak):
    global steps_open
    weather = fog_or_sun(ldr.value * 10)
    if weather == "fog":
        if fog_streak == 0:
            step_motor_clockwise(steps_open)
        fog_streak += 1
        sun_streak = 0
        print("Fog Detected!")
    else:
        if sun_streak == 0 and fog_streak > 0:
            step_motor_anticlockwise(steps_open)
        sun_streak += 1
        fog_streak = 0
        print("Sunlight Detected!")
    return fog_streak, sun_streak

try:
    while True:
        fog_streak, sun_streak = motor_on_weather(ldr, fog_streak, sun_streak)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    cleanup_motor()
    print("Exited Properly.")