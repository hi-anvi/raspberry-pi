# Raspberry Pi Repository

This repository has got some of my Raspberry Pi 5 projects I have made on my pi and some of the errors that I have encountered with my pi.

## Getting started

These steps will help you access your raspberry pi desktop and ssh into your pi wirelessly on Mac.

### Components

Here is the list of things you will require to ssh into your pi:

* Raspberry Pi
* Type C charger (official pi adapter is reccommended)
* Micro SD card
* Micro SD card adapter to Mac
* Optional but reccommended: Raspberry Pi case, raspberry pi cooler etc.

<img width="768" height="728" alt="image" src="https://github.com/user-attachments/assets/2560d5ed-256d-44d3-9a3f-9deaeac7ef88" />

### Step 1: Install the RPi Imager

Go to the [site](https://www.raspberrypi.com/software/), scroll down and click "Download for macos". Open it.

### Step 2: Setup the SD card

Insert the SD card into your macos and note down the name of it.
After openning the imager, there will be 3 options and select the following for each option:

* Choose Device: Raspberry Pi 5 (If you have some other Pi, choose that)
* Choose OS: Raspberry Pi 64 bit
* Choose Storage: The name of the SD card you noted down.

Click on write and click on edit settings. You should see something like this:

<img width="710" height="856" alt="image" src="https://github.com/user-attachments/assets/f8d904a4-90ca-43cd-addf-39b1d0611cd7" />

* Tick everything and fill in the details, respectively. Note down the hostname, username and password somewhere. NOTE: Lan is the Wi-Fi.
* Go to sevices on the top and enable ssh. 
* Click save. You will be brought back to the original place where you clicked edit setting but now you will click yes.

The writing proccess will start now.

### Step 3: Boot the RPi

Once the writing proccess completes, eject the SD card safely from your mac and put it into you RPi here:

<img width="918" height="572" alt="image" src="https://github.com/user-attachments/assets/437f6b17-ec38-4f63-a998-c1593884b72f" />

* Plug in the power cable into the pi and give it power.
* If you see a red light, click the button next to it (not using case) for 5 seconds and you should see a green light.
* Wait for a few minutes so that the raspberry pi can boot up properly.

### Step 4: SSH into the Raspberry Pi

Open your mac terminal and type the following command:

```
ssh <username>@<hostname>.local
```

Replace <username> with the username you used while setting up the SD card and replace <hostname> with the hostname you used while setting up
the SD card.

* It will prompt you for the password of your pi, enter it correctly.
* If successful, you will be in your pi terminal.

### Step 5: Access the RPi Desktop

In your pi terminal type the following command:

```
sudo apt update && sudo apt upgrade -y
```

This will update your pi. 
After the update is done, type:

```
sudo apt install rpi-connect-lite
```

This is necessary to access the Desktop of the pi.
Please make sure you have an account on [this site](https://www.raspberrypi.com/software/connect/) before running the command below.

To start the process, type:

```
rpi-connect on
```

Then type:

```
rpi-connect signin
```

* This will give you a link.
* Click on it.
* Give a name to the pi.
* Go back to the terminal

The terminal should show that the signin was successful.
Go to the [site](https://connect.raspberrypi.com/devices)

Connect via -> Screen sharing

You should be able to the the the Desktop of the pi in a few minutes.
