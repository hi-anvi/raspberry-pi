# Imports needed modules
import cv2 # for analyzing image
import time # to help keep led on/off for aprropiate time
import csv # to put analyzed data somewhere
from gpiozero import LED # for led control
import os
import sys
import argparse
import glob
import numpy as np
import pandas as pd
from ultralytics import YOLO

# Define and parse user input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Path to YOLO model file (example: "runs/detect/train/weights/best.pt")',
                    required=True)
args = parser.parse_args()

# Parse user inputs
model_path = args.model

# Check if model file exists and is valid
if (not os.path.exists(model_path)):
    print('ERROR: Model path is invalid or model was not found. Make sure the model filename was entered correctly.')
    sys.exit(0)

# Load the model into memory
model = YOLO(model_path, task='detect')

# Vehicle list
vehicle_num = [1, 2, 3, 4, 5, 6, 7, 8, 36]

# Writes header in the csv
csv_file = open('traffic_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Road', 'Number of Vehicles', 'Red Light Duration', 'Green Light Duration'])

# Sets up dictonaries for lane and important info
road1 = {
    "road": "road 1",
    "No of cars": 0,
    "Green light": 0,
    "Red light led": LED(2),
    "Green light led": LED(3)
}

# Important Functions

def get_img(cap):
    """Returns the image"""
    # Clicks the image
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        return 0
    return img
def process_results(results):
    """Returns a list with the the classes"""
    # Initialize an empty DataFrame
    df = pd.DataFrame(columns=['x', 'y', 'width', 'height', 'confidence', 'class'])

    # Process the results
    for r in results:
        if r.boxes is not None:
            # Convert the boxes to a DataFrame
            boxes_df = pd.DataFrame(r.boxes.data.tolist(), columns=['x', 'y', 'width', 'height', 'confidence', 'class'])
            df = pd.concat([df, boxes_df], ignore_index=True)
    return df

def find_vehicles(class_list):
    """Returns a list with all the vehicles found"""
    # Finds all vehicles in detections
    vehicles = []

    for clas in range(len(class_list)):
        if class_list[clas] in vehicle_num:
            vehicles.append(class_list[clas])

    return vehicles

def lighting_control(road1):
    """Sets lighting, returns nothing"""
    road1["Green light led"].on()
    road1["Red light led"].off()
    time.sleep(road1["Green light"])
    road1["Green light led"].off()
    road1["Red light led"].on()
    time.sleep(5)

# Set camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Main body

print("Starting...")

try:
    while True:

        # Clicks the image
        img = get_img(cap)

        # Run inference
        results = model(img)

        # Process results to a DataFrame
        df = process_results(results)

        # Print the DataFrame
        df.to_csv("model_results.csv")
        class_list = df['class'].to_list()

        # Finds all vehicles in detections
        vehicles = find_vehicles(class_list)
        road1["No of cars"] = len(vehicles) # puts no of vehicles in dictionary

        # Calculates the time needed for green light
        road1["Green light"] = max(3, round(1.25 * int(road1["No of cars"])))

        # Puts data in csv file
        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), road1["road"], road1["No of cars"], 5, road1["Green light"]])

        # Set the LEDs accordingly
        lighting_control(road1)

except KeyboardInterrupt:
    pass

finally:
    road1["Green light led"].off()
    road1["Red light led"].off()
    cv2.destroyAllWindows()
    csv_file.close()

print("Exiting...")