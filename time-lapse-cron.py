
import datetime
import os

OUTPUT_DIR =  '/home/camera/output'

try:
    import picamera
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
except picamera.exc.PiCameraMMALError:
    exit()
 
current_time = datetime.datetime.now()

# set the directory to store the captured photo in, and create if doesn't exist
DAILY_DIR = os.path.join(OUTPUT_DIR, current_time.strftime("%Y-%m-%d"))

if not os.path.isdir(DAILY_DIR):
    os.makedirs(DAILY_DIR)

# actually capture the photo
camera.capture(os.path.join(DAILY_DIR,
                            current_time.strftime("%Y-%m-%d-%H-%M-%S")+'.jpg'))
