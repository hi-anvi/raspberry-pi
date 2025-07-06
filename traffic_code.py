# Imports needed modules
from picamera2 import Picamera2 # for ai camera
import torch # for analyzing image
import cv2 # for analyzing image
import time # to help keep led on/off for aprropiate time
import csv # to put analyzed data somewhere
from gpiozero import LED # for led control
import RPi.GPIO as GPIO # for controlling motor

# Vehicle list
vehicle_classes = ['car', 'bus', 'truck', 'motorcycle', 'bicycle']

# Stepper motor ULN2003 IN1-IN4
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Writes header in the csv
csv_file = open('traffic_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Road', 'Number of Vehicles', 'Green Light Duration'])

# Sets up dictonaries for lane and important info
road1 = {
    "road": "road 1",
    "No of cars": 0,
    "Green light": 0,
    "Red light led": LED(2),
    "Green light led": LED(3)
}
road2 = {
    "road": "road 2",
    "No of cars": 0,
    "Green light": 0,
    "Red light led": LED(4),
    "Green light led": LED(5)
}
road3 = {
    "road": "road 3",
    "No of cars": 0,
    "Green light": 0,
    "Red light led": LED(6),
    "Green light led": LED(12)
}
road4 = {
    "road": "road 4",
    "No of cars": 0,
    "Green light": 0,
    "Red light led": LED(13),
    "Green light led": LED(16)
}
roads = [road1, road2, road3, road4]

# Setup GPIO for motor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in [IN1, IN2, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)

# Stepper motor half-step sequence
SEQ = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Stepper motor functions

def step_motor(steps, delay=0.002):
    """Move motor by number of steps"""
    if steps > 0:
        seq = SEQ
    else:
        seq = SEQ[::-1]
        steps = -steps
    for _ in range(steps):
        for pattern in seq:
            GPIO.output(IN1, pattern[0])
            GPIO.output(IN2, pattern[1])
            GPIO.output(IN3, pattern[2])
            GPIO.output(IN4, pattern[3])
            time.sleep(delay)

def cleanup_motor():
    """Turn off all motor coils"""
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)


# Get camera and set it up
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
time.sleep(2)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

try:
    for i in range(len(roads)):

        # Makes motor rotate 90 degrees
        if i != 0:
            step_motor(STEPS_90)

        # Clicks the image
        img = picam2.capture_array()

        # Convert to BGR
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Run inference
        results = model(img_bgr)
        detections = results.pandas().xyxy[0]  # finds out which are vehicles
        vehicles = detections[detections['name'].isin(vehicle_classes)] # gives types of vehicles
        roads[i]["No of cars"] = len(vehicles) # puts no of vehicles in dictionary

        # Calculates the time needed for green light
        roads[i]["Green light"] = max(5, round(0.75 * roads[i]["No of cars"]))

        # Puts data in csv file
        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), roads[i]["road"], roads[i]["No of cars"], roads[i]["Green light"]])

        # Sets the lights accordingly
        roads[0]["Red light led"].on()
        roads[1]["Red light led"].on()
        roads[2]["Red light led"].on()
        roads[3]["Red light led"].on()
        roads[i]["Green light led"].on()
        roads[i]["Red light led"].off()

        # Keeps green light on for that time period
        time.sleep(roads[i]["Green light"])

        # Makes it red again when it is time
        roads[i]["Red light led"].on()

    # Return to original position after 4 roads
    step_motor(-128 * 3)

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
    csv_file.close()
    for r in roads:
        r["Red light led"].off()
        r["Green light led"].off()

print("Exiting...")

# Stops the picam
picam2.stop()

# Clean up any GPIO
GPIO.cleanup()
