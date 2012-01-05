#!/usr/bin/env python

import os, sys, shutil, datetime

class DocSort:
    def __init__(self, source_dir, target_dir, age_seconds):
        for f in os.listdir(source_dir):
            
            file_name = source_dir + '/' + f
            if not os.path.isfile(file_name):
                print file_name, 'is not a regular file'
                continue

            print 'Processing', file_name
            mtime = int(os.stat(file_name).st_mtime)
            date = datetime.datetime.fromtimestamp(mtime)

            if (datetime.datetime.now() - date) < datetime.timedelta(0, age_seconds):
                print 'Skipping', file_name, '(%s)' % (date, )
                continue
            
            dir = target_dir + '/' + '%04d' % (date.year, )
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            dir = dir + '/' + '%02d' % (date.month, )
            if not os.path.exists(dir):
                os.makedirs(dir)

            try:
                shutil.move(file_name, dir)
            except:
                e = sys.exc_info()[1]
                print(str(e))

def usage():
    print 'usage: %s source_dir target_dir <age_seconds>' % (sys.argv[0], )
    sys.exit(2)
    
if __name__ == '__main__':

    if len(sys.argv) < 3:
        usage()

    if len(sys.argv) > 3:
        try:
            age_seconds = int(sys.argv[3])
        except:
            usage()
    else:
        age_seconds = 2419200
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    for dir in [source_dir, target_dir]:
        if not os.path.isdir(dir) or not os.access(dir, os.R_OK):
            usage()

    ds = DocSort(source_dir, target_dir, age_seconds)
    
