import os
import datetime
import pytz
import subprocess

from dateutil import parser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL.ExifTags import TAGS
from shutil import copy2

ROOT_DIR = "/home/alex/data/photos/2016/2016-timelapse02-rpi/"
OUTPUT_DIR = "/home/alex/temp/timelapse/"
HOURS_TO_EXTRACT = [(9,30), 
                    (10,00), 
                    (10,30), 
                    (11,00), 
                    (11,30), 
                    (12,00), 
                    (12,30),
                    (13,00),
                    (13,30), 
                    (14,00),
                    (14,30), 
                    (15,00),
                    (15,30),
                    (16,00)]
ADD_OVERLAY = False
FONT = ImageFont.truetype("FreeSansOblique.ttf", 120)
FRAMERATE = 10

dirs = sorted(os.listdir(ROOT_DIR))

photos = []

def get_exif(i):
    ret = {}
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret, True
    else:
        return None, False

# get the paths to the relevant dirs
for d in dirs:
    if d.startswith("00"):
	continue

    daily_photos = sorted(os.listdir(os.path.join(ROOT_DIR,d)))

    for dp in daily_photos:
	(year, month, day, hour, minute, second) = dp.split("-")
	for h,m in HOURS_TO_EXTRACT:
	    if int(h) == int(hour) and int(minute) == int(m):
		photos.append(os.path.join(ROOT_DIR,d,dp))

for counter, p in enumerate(photos):
    filename =  "image%04d.jpg" % (counter + 1)
    print filename
    copy2(p,os.path.join(OUTPUT_DIR,filename))
    
    if ADD_OVERLAY:
        img = Image.open(os.path.join(OUTPUT_DIR,filename))
        draw = ImageDraw.Draw(img)
    
        date_string = ""
        exif_tags, result = get_exif(img)
        if result:
            exif_date = exif_tags['DateTimeOriginal'] 
            date = parser.parse(exif_date)
            date_string = date.strftime('%B')
    
        img_w, img_h = img.size
    
        text_x = img_w - 700
        text_y = img_h - 200
    
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((text_x, text_y),date_string,(255,255,255),font=FONT)

        img.save(os.path.join(OUTPUT_DIR,filename))

# Finally create the actual video

video_generator_command = "ffmpeg -framerate %d -i %s/image%%04d.jpg -c:v libx264 -r %d %s/outputfile.mp4" % (int(FRAMERATE), OUTPUT_DIR, int(FRAMERATE), OUTPUT_DIR ) 
subprocess.call(video_generator_command, shell=True) 
