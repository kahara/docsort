#!/usr/bin/env python


import unittest, time, datetime, tempfile, os, sys, shutil, uuid, random, json, syslog
from docsort import DocSort

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DocSortTest('test_docsort'))
    return suite

class DocSortTest(unittest.TestCase):

    # http://stackoverflow.com/a/553448
    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime 
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return (start + datetime.timedelta(seconds=random_second))
    
    def setUp(self):
        # generate a bunch of (empty) files of varying creation dates
        self.target_dir = tempfile.mkdtemp()
        #print 'Target dir', self.target_dir
        self.source_dir = self.target_dir
        #print 'Source dir', self.source_dir
        self.start_date = datetime.datetime.utcnow() - datetime.timedelta(3650) # about ten years ago
        self.end_date = self.start_date + datetime.timedelta(7300) # about ten years from now
        #print 'Date from\t', self.start_date, '\nto\t\t', self.end_date

        # xxx create more files closer to the last few months (or something)
        self.count = 10
        self.filetree = {}        
        for i in range(0, self.count):
            file_uuid = uuid.uuid4().hex
            file_name = self.source_dir + '/' + file_uuid
            open(file_name, 'w').close()
            date = self.random_date(self.start_date, self.end_date)
            epoch  = int(time.mktime(date.timetuple()))
            os.utime(file_name, (epoch, epoch))

            continue
            
            if not date.year in self.filetree:
                self.filetree[date.year] = {}
            if not date.month in self.filetree[date.year]:
                self.filetree[date.year][date.month] = {}
            self.filetree[date.year][date.month][file_uuid] = int(epoch)
        #print json.dumps(self.filetree, sort_keys=True, indent=4)
                            
    def tearDown(self):
        #shutil.rmtree(self.target_dir)
        pass
    
    def test_docsort(self):
        #ds = DocSort(self.source_dir, self.target_dir, 40320) # four weeks
        
        for yk, yv in self.filetree.iteritems():
            for mk, mv in yv.iteritems():
                for ik, iv in mv.iteritems():
                    file_name = self.target_dir + '/%04d/%02d/%s' % (yk, mk, ik)

                    try:
                        mtime = int(os.path.getmtime(file_name).st_mtime)
                        print mtime
                    except:
                        e = sys.exc_info()[1]
                        syslog.syslog(str(e))
                        continue

                    print 'Checking %04d %02d %s %d %d' % (yk, mk, ik, iv, mtime)
                    if mtime != iv:
                        print 'Incorrect timestamp in', file_name, mtime, iv
                    else:
                        print 'MATCH'

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
    
