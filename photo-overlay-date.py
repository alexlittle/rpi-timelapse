
import datetime
import os
import pytz

from dateutil import parser

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from PIL.ExifTags import TAGS


ROOT_DIR = "/home/alex/temp/timelapse/"

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

photos = os.listdir(ROOT_DIR)
font = ImageFont.truetype("FreeSansOblique.ttf", 120)

for p in photos:
	img = Image.open(os.path.join(ROOT_DIR,p))
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
	draw.text((text_x, text_y),date_string,(255,255,255),font=font)

	img.save(os.path.join(ROOT_DIR,p))



