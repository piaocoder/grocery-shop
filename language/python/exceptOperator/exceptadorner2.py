def decorator_whith_params_and_func_args(arg_of_decorator):
    print '11111111111111'
    def handle_func(func):
        print '2222222222'
        def handle_args(*args, **kwargs):
            print '333333333333333'
            print "begin"
            func(*args, **kwargs)
            print "end"
            print arg_of_decorator, func, args,kwargs
        return handle_args
    return handle_func

def decorator_whith_params_and_func_args1(arg_of_decorator):
    print '11111111111111'
    def handle_func(func, *args, **kwargs):
        print '333333333333333'
        print "begin"
        func(*args, **kwargs)
        print "end"
        print arg_of_decorator, func, args,kwargs
    return handle_func

def decorator_test1(func):
    def handle_func(*args, **kwargs):
        print 'begin'
        func(args, kwargs)
        print 'end'
    return handle_func

class TestA(object):
    def __init__(self):
        self._str = '123'

    @decorator_whith_params_and_func_args("123")
    def foo4(self, a, b=2):
        print "Content"

import pdb
pdb.set_trace()
testA = TestA()
testA.foo4(1, b=3)
