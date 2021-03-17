import os
import datetime
import pytz
import subprocess
import fnmatch

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL.ExifTags import TAGS
from shutil import copy2
from datetime import date, timedelta

YEARS = [2017]
OUTPUT_DIR = os.path.join("/home/alex/temp/timelapse/", str(YEARS[0]))
ADD_OVERLAY = True
FONT = ImageFont.truetype("FreeSansOblique.ttf", 100)
FRAMERATES = [15]


def find_files(base, pattern):
    
    if os.path.isdir(base):
        '''Return list of files matching pattern in base folder.'''
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
            os.path.isfile(os.path.join(base, n))]
    else:
        return []

photos = []

for year in YEARS:

    year_dir = os.path.join('/home/alex/data/photos',str(year),str(year)+'-timelapse') 
    dirs = sorted(os.listdir(year_dir))
    
    d1 = date(year, 1, 1)  # start date
    d2 = date(year, 12, 31)  # end date

    delta = d2 - d1         # timedelta

    for i in range(delta.days + 1):
        for hour in range(0,24):
            for minute in [0,15,30,45]:
                photo = {}
                file_search = '%s-%02d-%02d' % (d1 + timedelta(i), hour, minute)
                base = year_dir + '/' + str(d1 + timedelta(i)) + '/'
                pattern = file_search + '*.jpg'
                results = find_files(base, pattern)
                
                if len(results) > 0:
                    if not os.path.isdir(results[0]):
                        photo['night'] = False
                        photo['path'] = base
                        photo['filename'] = results[0]
                        photos.append(photo)
                elif hour < 7 or hour > 21:
                    photo['night'] = True    
                    photo['filename'] = file_search
                    photos.append(photo)
    
for counter, photo in enumerate(photos):
    
    filename = "image%05d.jpg" % (counter + 1)
    
    print("processing: %s as %s" % (photo['filename'], filename ))
    
    if not photo['night']:
        
        try:
            copy2(os.path.join(photo['path'],photo['filename']),os.path.join(OUTPUT_DIR,filename))
            
            if ADD_OVERLAY:
                img = Image.open(os.path.join(OUTPUT_DIR,filename))
                draw = ImageDraw.Draw(img)
            
                (year, month, day, hour, minute, second) = photo['filename'].split("-")
                date = datetime.datetime(int(year), int(month), int(day), int(hour))
                date_string = date.strftime('%d %B %Y')
            
                img_w, img_h = img.size
            
                text_x = img_w - 1000
                text_y = img_h - 200
            
                draw.text((text_x, text_y),date_string,(0,0,0),font=FONT)
        
                img.save(os.path.join(OUTPUT_DIR,filename))
        except OSError:
            pass
        
    else:
        img = Image.new('RGB', (2592,1944))
        if ADD_OVERLAY:
            draw = ImageDraw.Draw(img)
        
            (year, month, day, hour, minute) = photo['filename'].split("-")
            date = datetime.datetime(int(year), int(month), int(day), int(hour))
            date_string = date.strftime('%d %B %Y')
        
            img_w, img_h = img.size
        
            text_x = img_w - 1000
            text_y = img_h - 200
        
            draw.text((text_x, text_y),date_string,(255,255,255),font=FONT)
            
        img.save(os.path.join(OUTPUT_DIR,filename))
        
        
        
for framerate in FRAMERATES:
    video_generator_command = "ffmpeg -framerate %d -i %s/image%%05d.jpg -c:v libx264 -r %d %s/%d-outputfile-%dfps.mp4" % (int(framerate), OUTPUT_DIR, int(framerate), OUTPUT_DIR, YEARS[0], framerate ) 
    subprocess.call(video_generator_command, shell=True) 
    

    
