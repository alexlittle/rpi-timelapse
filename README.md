# rpi-timelapse

For creating timelapse videos from photos with a Raspberry Pi with camera
module.

Latest version of the video I have produced: https://www.youtube.com/watch?v=71Q9xi8Dmik


time-lapse-cron.py
------------------
File to put on the Raspberry Pi, then set up a cron task to run this script
regularly (e.g. every 15-30 mins)

With a 16Gb SD card (where the OS is also installed), it'll fit about 6-8 weeks
of photos when they're taken every 15 mins (day and night). So you'll likely
need to download the photos to another device fairly regularly.

For the photos that are taken overnight (or very low light), I tend to just
delete these, as they're not any use for creating a video. From the setup and
config I have, I'm pretty confident about removing any photo that is under 1.5Mb
in filesize, so I have a command to delete these automatically. The command I
use is ``find . -name "*.jpg" -size -1500k -exec mv {} /home/alex/temp/tl-erase/ \;``
- but use this command with a *lot* of caution, from exactly the right 
directory, otherwise you could remove jpg images on your system that you really
want to keep.


extract-photos.py
-----------------
Takes the directories of where the photos have been stored, extracts the ones
requested (based on the hour/min) and stitches altogether into an mp4 video.
Ffmeg is used, so you'll need that installed, or alter the video processing part
to use another tool.
