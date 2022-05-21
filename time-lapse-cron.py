import datetime
import os


OUTPUT_DIR =  '/home/alex/timelapse/output'

current_time = datetime.datetime.now()

# set the directory to store the captured photo in, and create if doesn't exist
DAILY_DIR = os.path.join(OUTPUT_DIR, current_time.strftime("%Y-%m-%d"))

if not os.path.isdir(DAILY_DIR):
    os.makedirs(DAILY_DIR)

out_file = os.path.join(DAILY_DIR, current_time.strftime("%Y-%m-%d-%H-%M-%S")+'.jpg')

os.system('libcamera-jpeg -o %s' % out_file)
