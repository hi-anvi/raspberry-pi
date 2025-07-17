# Write your code here :-)
# Random list generator

import random
from gpiozero import LED

def random_no_of_vehicles(dictionary):
    """Returns a dictonary with random no of vehicles between 1 and 20"""
    num_vehicles = random.randint(1, 20)
    dict_updated = {}
    for key in dictionary:
        dict_updated[key] = dictionary[key]
    dict_updated["No. of vehicles"] = num_vehicles
    return dict_updated

def random_timestamp(dictionary):
    """Returns a dictionary with random timestamp"""
    dict_updated = {}
    year = "2025"
    month = str(random.randint(1, 12))
    date = str(random.randint(1, 31))
    hour = str(random.randint(0, 23))
    mins = str(random.randint(0, 59))
    sec = str(random.randint(0, 59))
    while month == 2 and date > 28 or month in [2, 4, 6, 9, 11] and date == 31:
        date = rand.randint(1, 31)
    for key in dictionary:
        dict_updated[key] = dictionary[key]
    timestamp = year + "-" + month + "-" + date + " " + hour + ":" + mins + ":" + sec
    dict_updated["Timestamp"] = timestamp
    return dict_updated

def green_light_time(dictionary):
    """Returns a dictionary with the green light time according to the no of vehicles"""
    dict_updated = {}
    num_cars = dictionary["No. of vehicles"]
    green_time = max(3, 1.25 * int(num_cars))
    for key in dictionary:
        dict_updated[key] = dictionary[key]
    dict_updated["Green light time"] = green_time
    return dict_updated

def rand_dict_creator():
    """Returns a total random dictionary with some parameters"""
    rand_dict = {}
    rand_dict = random_no_of_vehicles(rand_dict)
    rand_dict = random_timestamp(rand_dict)
    rand_dict = green_light_time(rand_dict)
    return rand_dict