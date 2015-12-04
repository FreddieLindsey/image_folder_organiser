#!/usr/bin/env python

import os, sys
from PIL import Image

if (len(sys.argv) < 3):
    print "Usage: ./main.py <file/folder to process> <destination for corrupt images>"
    exit(1)

jpgfile = Image.open(sys.argv[1])
