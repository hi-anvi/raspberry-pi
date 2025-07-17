from picamera2 import Picamera2
import cv2

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

print("Press 'q' in the video window to exit.")

# Main loop to display live video
while True:
    frame = picam2.capture_array()
    cv2.imshow("Picamera2 Live Feed", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()