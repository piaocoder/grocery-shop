#!/usr/bin/python
# coding:utf-8
"""
    作者意图：
        使用对象池来自由的控制对象的销毁，但是对于gc类语言来说，
        尽可能少的使用__del__（不能准确的预知内存释放的时间）
"""

import webdriver

class browser(object):
    instances = []
    def __new__(cls):
        for i in browser.instances:
            if i.occupied==False:
                i.occupied=True
                return i
        else:
            x = super(browser, cls).__new__(cls)
            browser.instances.append(x)
            return x

    def __init__(self):
        self.occupied = True
 
        if not hasattr(self, 'driver'):
            self.driver = webdriver.Firefox()
        self.driver.get('https://www.baidu.com/')
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(3)
 
    def quit(self):
        self.occupied = False
 
    def __del__(self):
        self.driver.quit()


class A(object):
    """Test Class"""
    def __init__(self):
        self._browser = browser()
        self._driver = self._browser.driver

    def __del__(self):
        """delete"""
        self._browser.quit()


if __name__ == '__main__':
    """main"""
    a1 = A()
    a2 = A()
