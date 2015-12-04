#!/usr/bin/env python

import os, sys
from PIL import Image

####################################
############ CONSTANTS #############
####################################

raw_exts = ['.arw', '.cr2']

####################################
############ FUNCTIONS #############
####################################

def makeFileDirectory(file_path):
    file_dirs=file_path.split('/')
    i = 0
    if (file_dirs[0] == ''):
        i += 1
    while (i < len(file_dirs) - 1):
        current_dir = "/".join(file_dirs[:i + 1])
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        i += 1

def createDirectory(file_path):
    makeFileDirectory(file_path)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

def doesDNGExist(file_path):
    for i in raw_exts:
        dng_path = file_path.replace(i, '.dng')
        if os.path.exists(dng_path):
            return True # os.path.getsize(dng_path) > os.path.getsize(file_path)
    return False

def moveDuplicates(folder_in, folder_out):
    if not os.path.exists(folder_in):
        print 'Folder to process does not exist, where is {0}?'.format(folder_in)
        exit(1)
    createDirectory(folder_out)
    for root, dirnames, filenames in os.walk(folder_in):
        for filename in filenames:
            if folder_out in os.path.join(root, filename) or '.DS_Store' in filename or '.dng' in filename:
                continue
            filename_joined = os.path.join(root, filename)
            if doesDNGExist(filename_joined):
                try:
                    os.rename(filename_joined, filename_joined.replace(folder_in, folder_out))
                except Exception:
                    print "Error processing {0}".format(filename_joined)

####################################
############ MAIN ##################
####################################

if (len(sys.argv) != 2):
    print 'Usage: ./main.py <folder to process>'
    exit(1)

moveDuplicates(sys.argv[1], '{0}/_images_to_delete'.format(sys.argv[1]))
