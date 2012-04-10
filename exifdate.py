#!/usr/bin/python

#    Copyright 2012 Benjamn Weißenfels b.pixeldrama@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script is inspired by the script from Gari Araolaza:
# http://eibar.org/blogak/teknosexua/archive/2011/02/23/how-to-fix-htc-tattoos-picture-timestamp

# Samsung Galaxy GT-S560 timestamps are buggy. This program solves
# this problem in your photos
# 
# Dependencies: You will need pyexiv2 library (v 3.0 )installed on your system to run it
#
#
# Usage:  python exifseconds.py <PATH_TO_FIX_FILES>


 

import sys, os
import pyexiv2
import re

pattdash = ("[0-9][0-9][0-9][0-9]:[0-9][0-9]:[0-9][0-9]\ [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\ ")
pattern = re.compile(pattdash)
tagnames = ['Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized']

def get_images_from_path(basepath):
    image_list = []
    for root, subdirs, files in os.walk(basepath):
        for file in files:
            if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
                image_list.append(os.path.join(root, file))
    return image_list          

def fix_date_time(image_path, tagname):
    try:
        metadata = pyexiv2.ImageMetadata(image_path)
        metadata.read()
    except IOError: 
        print "IOError: ", image_path
        return
    except UnicodeDecodeError:
        print "UnicodeDecodeError: ", image_path
        return
    try:
        tag = metadata[tagname]
        raw = tag.raw_value
    except:
        tag = None

    if tag != None and type(raw) == type('') and pattern.match(raw):
        corrected_string = raw.replace("-", ":")
        tag.value = corrected_string[:-1] #seems to be one char too much
        metadata.write()
        print "fixed: ", image_path.split('/')[-1], 

def main(argv):
    if len(argv)<2:
        print """This program fixes invalid DateTime stamps, 
replaces hyphens with colon. Specially created to be used
with pictures from the Galaxy GT-S5660."""
        return
    
    image_list = get_images_from_path(argv[1])

    for image_path in image_list:
        for tagname in tagnames:
            print "try to fix:", image_path
            fix_date_time(image_path, tagname)        

if __name__ == "__main__":
    main(sys.argv)
