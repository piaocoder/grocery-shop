class A(object):
    def __init__(self, flag):
        self.quitFlag = flag

    def set_flag(self):
        print '1:', id(self.quitFlag)
        self.quitFlag = "quit"
        print '2:', id(self.quitFlag)

flag1 = "exit"
print '0:', id(flag1)
aObj = A(flag1)
aObj.set_flag()
print '4:', id(flag1)
