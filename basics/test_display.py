 Import modules
from gpiozero import LED
import time

# Set GPIO pins for each LED from 'a' to 'g'
segments = {
    'a': LED(4),
    'b': LED(5),
    'c': LED(12),
    'd': LED(13),
    'e': LED(17),
    'f': LED(18),
    'g': LED(27)
}

# Segements to make number 0-9 respectively
numbers = {
    0: 'abcdef',
    1: 'bc',
    2: 'abged',
    3: 'abgcd',
    4: 'fgbc',
    5: 'afgcd',
    6: 'afgcde',
    7: 'abc',
    8: 'abcdefg',
    9: 'abcdfg'
}

# Define function to display the number given
def display_number(num):
    """Displays the light if number is less than 10. Returns 0 if number is too big."""
    if num >= 10:
        print("Error! Number too big. Please give a single digit number. Please try again.")
        return 0

    for segment in segments.values():
        segment.off()

    for letter in numbers[num]:
        segments[letter].on()

# Turn off all lights
def off_all():
    """Turns off all lights"""
    for segment in segments.values():
        segment.off()

# Tells user that you are good to go
print("Starting...")

# For loop which displays numbers from 0 - 9
for i in range(10):
    print("Number displayed: " + str(i))
    display_number(i)
    time.sleep(2)

# Set to exit
off_all()

print("Exiting...")