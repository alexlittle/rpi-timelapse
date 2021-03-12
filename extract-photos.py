import os
import datetime
import pytz
import subprocess

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL.ExifTags import TAGS
from shutil import copy2

YEARS = ["/media/alex/Seagate Expansion Drive/timelapse/2016-timelapse/",
         "/media/alex/Seagate Expansion Drive/timelapse/2017-timelapse/",
         "/media/alex/Seagate Expansion Drive/timelapse/2018-timelapse/",
         "/media/alex/Seagate Expansion Drive/timelapse/2019-timelapse/",
         "/media/alex/Seagate Expansion Drive/timelapse/2020-timelapse/",
         "/home/alex/data/photos/2021/2021-timelapse"]
OUTPUT_DIR = "/home/alex/temp/timelapse/"
HOURS_TO_EXTRACT = [(9,00)
					]
ADD_OVERLAY = True
FONT = ImageFont.truetype("FreeSansOblique.ttf", 100)
FRAMERATES = [10,15]



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


for year_dir in YEARS:

    dirs = sorted(os.listdir(year_dir))
    # get the paths to the relevant dirs
    for d in dirs:
        if d.startswith("00"):
    	    continue
    
        daily_photos = sorted(os.listdir(os.path.join(year_dir,d)))
    
        for dp in daily_photos:
            (year, month, day, hour, minute, second) = dp.split("-")
            for h,m in HOURS_TO_EXTRACT:
        	    if int(h) == int(hour) and int(minute) == int(m):
                     photo = {}
                     photo['path'] = os.path.join(year_dir,d,dp)
                     photo['filename'] = dp
                     photos.append(photo)

for counter, p in enumerate(photos):
    
    filename = "image%04d.jpg" % (counter + 1)
    print("processing: %s as %s" % (p['filename'], filename ))
    copy2(p['path'],os.path.join(OUTPUT_DIR,filename))
    
    if ADD_OVERLAY:
        img = Image.open(os.path.join(OUTPUT_DIR,filename))
        draw = ImageDraw.Draw(img)
    
        (year, month, day, hour, minute, second) = p['filename'].split("-")
        date = datetime.datetime(int(year), int(month), int(day), int(hour))
        date_string = date.strftime('%d %B %Y')
    
        img_w, img_h = img.size
    
        text_x = img_w - 1000
        text_y = img_h - 200
    
        draw.text((text_x, text_y),date_string,(0,0,0),font=FONT)

        img.save(os.path.join(OUTPUT_DIR,filename))

# Finally create the actual videos
for framerate in FRAMERATES:
	video_generator_command = "ffmpeg -framerate %d -i %s/image%%04d.jpg -c:v libx264 -r %d %s/outputfile-%dfps.mp4" % (int(framerate), OUTPUT_DIR, int(framerate), OUTPUT_DIR, framerate ) 
	subprocess.call(video_generator_command, shell=True) 
