import os
from shutil import copy

ROOT_DIR = "/home/alex/data/photos/2016/2016-timelapse02-rpi/"

OUTPUT_DIR = "/home/alex/temp/timelapse/"

HOURS_TO_EXTRACT = [10, 11, 12, 13, 14, 15]

dirs = os.listdir(ROOT_DIR)

photos = []

# get the paths to the relevant dirs
for d in dirs:
    if d.startswith("00"):
	continue

    daily_photos = os.listdir(os.path.join(ROOT_DIR,d))

    for dp in daily_photos:
	(year, month, day, hour, minute, second) = dp.split("-")
	for h in HOURS_TO_EXTRACT:
	    if h == int(hour) and int(minute) == 0:
		photos.append(os.path.join(ROOT_DIR,d,dp))

for p in photos:
    copy(p,OUTPUT_DIR)
