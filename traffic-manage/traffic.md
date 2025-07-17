# Traffic Management Project

Everyday, do you notice long traffic jams and the once the green light turns on, it is only for about a couple of seconds? Because this seems to happen in India alot now. This project is the 
solution I had. this is not fully complete right now but within some time you can run this on your Raspberry Pi 5. Right now this project can detect cars on one road, calculate the time which 
should be given for green light and give the appropiate time. NOTE: This project uses yolo11n.pt which will run on the pi.

## Getting Started

These instructions will get you a copy of the project up and running on your raspberry pi 5 for development and testing purposes.

### Prerequisites

If you don't have access the the Desktop of the Raspberry Pi, please take a look at the original [readme]{https://github.com/hi-anvi/raspberry-pi/readme.md}

### Installing

A step by step series of examples that tell you how to get a development env running

First of all, please follow the steps in this [youtube-link]{https://www.youtube.com/watch?v=z70ZrSZNi-8} to get the basic environment set up for the yolo detection of cars.

Later, install opencv and numpy if not already with this command:

```
sudo apt install python3-opencv python3-numpy
```

After the succesful installation, also install pandas with this command:

```
pip install pandas
```
Optional: If you want to, you can check if the installations were successful by running:

```
python3
```
This will open a python editor in the terminal and there type:

```
import numpy as np
import pandas as pd
import cv2
```
If they don't show any error, the installation was successful otherwise try again and verify if python3 and pip are installed in the pi env.

## Running the tests

Please copy-paste all the files here in the yolo folder and run traffic_manage_1road.py with this command:

```
python traffic_manage_1road.py --model=yolo11n_ncnn_model
```

Running algorithm.py:

```
python3 algorithm.py
```

### Break down into end to end tests

algorithm.py gets a random dictionary from random_dict_generator
traffic_manage_1road.py clicks an image, runs yolo object detection model, processes the results and puts the green light for that much time.
Please take a look at the comments and docstrings for more information on a script.

```
"""Returns the image"""
```

### And coding style tests

You will find comments everywhere in the code including docstrings. Some of the work here is not complete as this is an ongoing. You might 
find some short forms such as str for string, dict for dictionary

```
# Checks the max number of vehicles in the dict
```
## Authors

* **Anvi Gupta** - *Initial work* - [hi-anvi](https://github.com/hi-anvi)

See also the list of other projects like [mini-projects](https://github.com/hi-anvi/mini-projects) made by hi-anvi.

## Acknowledgments

* Hat tip to [youtube-video]{https://www.youtube.com/watch?v=z70ZrSZNi-8} for setting up the basic environment, PurpleBooth in git who helped me with the readme
* Inspiration: Traffic jams on the road
