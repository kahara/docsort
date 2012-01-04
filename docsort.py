#!/usr/bin/env python

import os, shutil, datetime

class DocSort:
    def __init__(self, source_dir, target_dir, file_age=40320):
        for f in os.listdir(source_dir):

            # xxx only process files older than file_age (seconds) ago
            file_name = source_dir + '/' + f
            if not os.path.isfile(file_name):
                print file_name, 'is not a regular file'
                continue
            print 'Processing', file_name
            mtime = int(os.stat(file_name).st_mtime)
            date = datetime.datetime.fromtimestamp(mtime)
            
            dir = target_dir + '/' + '%04d' % (date.year, )
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            dir = dir + '/' + '%02d' % (date.month, )
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            shutil.move(file_name, dir)

if __name__ == '__main__':
    dir = os.getcwd()
    print dir
    ds = DocSort(dir, dir)

