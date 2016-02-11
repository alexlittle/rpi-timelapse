
import datetime
import os

from time import sleep

OUTPUT_DIR =  '/home/camera/output'

try:
    import picamera
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
except picamera.exc.PiCameraMMALError:
    exit()


    
current_time = datetime.datetime.now()

DAILY_DIR = os.path.join(OUTPUT_DIR, current_time.strftime("%Y-%m-%d"))

if not os.path.isdir(DAILY_DIR):
    os.makedirs(DAILY_DIR)

camera.capture(os.path.join(DAILY_DIR,current_time.strftime("%Y-%m-%d-%H-%M-%S")+'.jpg'))
