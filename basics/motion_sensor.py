# Outputs data when motion sensor detects motion

# Imort modules
from gpiozero import MotionSensor
from signal import pause

# Gets motion sensor
motion_sensor = MotionSensor(4)

# Functions (refer to function name for info)
def motion():
    print("Motion detected")

def no_motion():
    print("Motion stopped")


print("Readying sensor...")

# Tells computer to run code when there is no motion
motion_sensor.wait_for_no_motion()

print("Sensor ready")

# Python eventListners
motion_sensor.when_motion = motion
motion_sensor.when_no_motion = no_motion

pause()