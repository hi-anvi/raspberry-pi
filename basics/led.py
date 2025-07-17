# Makes LED blink until program is stopped

# Import modules
from gpiozero import LED
from signal import pause

# Gets LED
led = LED(4)

# Makes LED blink every 1 second by calling blink method on it
led.blink()

pause()