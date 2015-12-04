#!/usr/bin/env python

import os, sys
import re
import subprocess
from PIL import Image

####################################
############ CONSTANTS #############
####################################

raw_exts = ['.arw', '.cr2']
duplicate_exts = raw_exts + ['.jpg']

corrupt_file = '_corrupt_file'
dng_found_or_created = '_dng_found_or_created'
duplicated_file = '_duplicate_file'
do_not_visit = [ corrupt_file, dng_found_or_created, duplicated_file ]

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

def doesDNGExistRAW(file_path):
    dng_path = file_path
    for i in raw_exts:
        insensitive_replace = re.compile(re.escape(i), re.IGNORECASE)
        dng_path = insensitive_replace.sub('.dng', dng_path)
    return file_path != dng_path and os.path.exists(dng_path)

def doesDNGExist(file_path):
    dng_path = file_path
    for i in duplicate_exts:
        insensitive_replace = re.compile(re.escape(i), re.IGNORECASE)
        dng_path = insensitive_replace.sub('.dng', dng_path)
    return file_path != dng_path and os.path.exists(dng_path)

def getFileList(folder_in):
    files_to_check = []
    for root, dirnames, filenames in os.walk(folder_in):
        for filename in filenames:
            add = True
            for i in do_not_visit:
                if i in os.path.join(root, filename):
                    add = False # Ignores processed directories
                    break
            if '.DS_Store' in filename:
                add = False
            if add: files_to_check.append(os.path.join(root, filename))
    return files_to_check

def convertNotDNGToDNG(file_list):
    for i in file_list:
        if '.dng' in i: continue
        if not doesDNGExistRAW(i) and '.{0}'.format(i.split('.')[-1]) in raw_exts:
            system_command = 'adobe_dng -c -fl'.split()
            system_command.append(i)
            process = subprocess.Popen(system_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if (process.communicate()[1] != ''):
                new_file = i.split('/')
                filename = new_file[-1]
                new_file = new_file[:-1]
                new_file.append('{0}/{1}'.format(corrupt_file, filename))
                new_file = '/'.join(new_file)
                makeFileDirectory(new_file)
                try:
                    os.rename(i, new_file)
                except Exception:
                    print "Error moving {0} to {1}".format(i, new_file)

def removeIfDNGPresent(folder_in, file_list, folder_out = ''):
    if (folder_out == ''):
        folder_out = '{0}/{1}'.format(folder_in, dng_found_or_created)
    for filename in file_list:
        dng_exists = doesDNGExist(filename)
        if dng_exists:
            new_file = filename.replace(folder_in, folder_out)
            makeFileDirectory(new_file)
            try:
                os.rename(filename, new_file)
            except Exception:
                print "Error moving {0} to {1}".format(filename, new_file)

def duplicateHunter(file_list):
    for i in file_list:
        filename, _ = os.path.splitext(i)
        similar_files = [file_ for file_ in file_list if filename in file_]
        for j in similar_files:
            if (i == j): continue
            if os.path.getsize(i) == os.path.getsize(j):
                file_list.remove(j)
                new_file = i.split('/')
                filename = new_file[-1]
                new_file = new_file[:-1]
                new_file.append('{0}/{1}'.format(duplicated_file, filename))
                new_file = '/'.join(new_file)
                makeFileDirectory(new_file)
                try:
                    os.rename(j, new_file)
                except Exception:
                    print "Error moving {0} to {1}".format(i, new_file)


####################################
############ MAIN ##################
####################################

if (len(sys.argv) != 2):
    print 'Usage: ./main.py <folder to process>'
    exit(10)

folder_in = sys.argv[1]

if not os.path.exists(folder_in):
    print 'Folder to process does not exist, where is {0}?'.format(folder_in)
    exit(11)

file_list = getFileList(folder_in)
convertNotDNGToDNG(file_list)
removeIfDNGPresent(folder_in, file_list)
duplicateHunter(getFileList(folder_in))
