#coding:utf-job
import unittest

class Widget(object): 
    def __init__(self, desc, size=(40,40)): 
        self.size = size 
        self.name = desc

    def getSize(self): 
        '''size'''
        return self.size 

    def resize(self, width, height): 
        '''resize'''
        if width <0 or height < 0: 
            raise ValueError, 'illegal size' 
        else: 
            self.size = (width, height) 
            return self.size 

    def dispose(self): 
        '''dispose'''
        pass

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
        self.widget = None

    def test_default_size(self):
        self.assertEqual(self.widget.getSize(), (40, 40), 'Incorrect default size')

    def test_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.getSize(), (100,150), 'wrong size after resize')

if __name__ == '__main__':
    '''main'''
    widgetTestSuite = unittest.TestSuite()
    widgetTestSuite.addTest(WidgetTestCase('test_default_size'))
    widgetTestSuite.addTest(WidgetTestCase('test_resize'))
    unittest.main()
