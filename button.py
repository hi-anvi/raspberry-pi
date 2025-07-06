# Gives different outputs when button is pressed, held and reeased

# Import modules from libraries
from gpiozero import Button
from signal import pause

# Gets button
button = Button(4)

# Function(refer to name to see what they do)
def button_pressed():
    print("Button was pressed")

def button_held():
    print("Button was held")

def button_released():
    print("Button was released")

# Tell what to do when something happens like in eventListners in node js
button.when_pressed = button_pressed
button.when_held = button_held
button.when_released = button_released

pause()