# Imports needed modules
import cv2 # for analyzing image
import time # to help keep led on/off for aprropiate time
import csv # to put analyzed data somewhere
from gpiozero import LED # for led control
import os
import numpy as np
import pandas as pd
import sys
from ultralytics import YOLO

# Parse user inputs
model_path = "yolo11n_ncnn_model"

# Check if model file exists and is valid
if (not os.path.exists(model_path)):
    print('ERROR: Model path is invalid or model was not found. Make sure the model filename was entered correctly.')
    sys.exit(0)

# Load the model into memory
model = YOLO(model_path, task='detect')

# Vehicle list
vehicle_num = [1, 2, 3, 4, 5, 6, 7, 8]

def get_img(cap):
    """Returns the image"""
    # Clicks the image
    for i in range(20):
        ret, img = cap.read()
        time.sleep(0.05)
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        return 0
    return img

# Makes results easier to use
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

# Helps find vehicles from classes
def find_vehicles(class_list):
    """Returns a list with all the vehicles found"""
    # Finds all vehicles in detections
    vehicles = []

    for clas in range(len(class_list)):
        if class_list[clas] in vehicle_num:
            vehicles.append(class_list[clas])

    return vehicles

def set_cam(num):
    """Sets up the usb camera"""
    # Set camera
    cap = cv2.VideoCapture(num)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def set_basics_img(img):
    """Returns mid_height and mid_width"""
    # Get image dimensions (height, width, channels)
    height, width = img.shape[:2]

    # Calculate the midpoint for vertical split
    mid_width = width // 2
    mid_height = height // 2

    # Save full image
    cv2.imwrite('full_image.jpg', img)

    return mid_height, mid_width


def get_dict(num):
    """Returns a dict depending on the road"""

    # Finds index of camera
    if num == 1 or num == 2:
        index = 0
    else:
        index = 2

    # Set camera
    cap = set_cam(index)

    # Captures the image
    img = get_img(cap)

    # Get mid_height and mid_width
    mid_height, mid_width = set_basics_img(img)

    # Define the dict
    rand_dict = {"Road": num}

    if num == 1:

        # Put correct LED lights
        rand_dict["Green led"] = LED(16)
        rand_dict["Red led"] = LED(13)

        # Fix mid_height variable
        mid_height = 160

        # Crop the bottom half
        img = img[mid_height:, :]

        # Save the image
        cv2.imwrite('1_half.jpg', img)

    elif num == 2:

        # Put correct LED lights
        rand_dict["Green led"] = LED(3)
        rand_dict["Red led"] = LED(2)

        # Fix mid_height variable
        mid_height = 160

        # Crop the top half
        img = img[:mid_height, :]

        # Save the image
        cv2.imwrite('2_half.jpg', img)

    elif num == 3:

        # Put correct LED lights
        rand_dict["Green led"] = LED(12)
        rand_dict["Red led"] = LED(6)

        # Fix mid_height variable
        mid_height = 207

        # Crop the bottom half
        img = img[:mid_height, :]

        # Save the image
        cv2.imwrite('3_half.jpg', img)

    elif num == 4:

        # Put correct LED lights
        rand_dict["Green led"] = LED(5)
        rand_dict["Red led"] = LED(4)

        # Fix mid_height variable
        mid_height = 207

        # Crop the top half
        img = img[mid_height:, :]

        # Save the image
        cv2.imwrite('4_half.jpg', img)

    # Run inference
    results = model(img)

    # Process results to a DataFrame
    df = process_results(results)

    # Convert DataFrame to a list
    class_list = df['class'].to_list()

    # Finds all vehicles in detections
    vehicles = find_vehicles(class_list)
    rand_dict["No of cars"] = len(vehicles) # puts no of vehicles in dictionary

    # Calculates the time needed for green light
    rand_dict["Green light time"] = max(3, round(1.25 * int(rand_dict["No of cars"])))

    return rand_dict
