# Makes buzzer emit sound every half second
# Note: Buzzer might not stop beeping after exiting the program
# If this happens, break the circuit

# Import modules
from gpiozero import Buzzer
from signal import pause

# Gets buzzer
buzzer = Buzzer(4)

# Gets buzzer to beep every half second by calling the beep method on it
buzzer.beep(0.5, 0.5)

pause()