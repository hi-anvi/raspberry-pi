# Alarm system on motion

# Import modules
from gpiozero import LED, Buzzer, MotionSensor
from signal import pause
import time

# Timestamp modules
import csv
from pathlib import Path
from datetime import datetime

# Gets electrical components
led = LED(14)
buzzer = Buzzer(15)
motion_sensor = MotionSensor(4)

# CSV file via Path
output_csv_path = Path("detected_motion.csv")

# Holds timestamps to be sent to CSV file
motion = {
    "start_time": None,
    "end_time": None,
}

# Method which writes timestamp to CSV file
def write_to_csv():
    first_write = not output_csv_path.is_file()

    with open(output_csv_path, "a") as file:
        field_names = motion.keys()
        writer = csv.DictWriter(file, field_names)
        if first_write:
            writer.writeheader()
        writer.writerow(motion)

# Function when motion starts
def start_motion():
    led.blink(0.5, 0.5)
    buzzer.beep(0.5, 0.5)
    motion["start_time"] = datetime.now()
    print("motion detected")

# Function when motion ends
def end_motion():
    if motion["start_time"]:
        led.off()
        buzzer.off()
        motion["end_time"] = datetime.now()
        write_to_csv()
        motion["start_time"] = None
        motion["end_time"] = None
    print("motion ended")

print("Warming up sensor...")

# Waits for 30 seconds
time.sleep(30)

print("Readying sensor...")

# Waits for no motion
motion_sensor.wait_for_no_motion()

print("Sensor ready")

# Python eventListeners
motion_sensor.when_motion = start_motion
motion_sensor.when_no_motion = end_motion

pause()