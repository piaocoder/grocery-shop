#coding:utf-job
import os
import unittest
import os.path
import tempfile

def rmTest(filename):
    '''remove a filename'''
    os.remove(filename)

class RmTestCase(unittest.TestCase):
    '''test case'''
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
 
    def setUp(self):
        with open(self.tmpfilepath, "wb") as f:
            f.write("Delete me!")
 
    def test_rm(self):
        # remove the file
        rmTest(self.tmpfilepath)
        # test that it was actually removed
        self.assertFalse(os.path.isfile(self.tmpfilepath), 
                "Failed to remove the file.")

class RmTestCaseMock(unittest.TestCase):
    '''remove filename by use mock'''
    @mock.patch('mymo

if __name__ == '__main__':
    '''main'''
    unitSuite = unittest.TestSuite()
    unitSuite.addTest(RmTestCase('test_rm'))
    unittest.main()
