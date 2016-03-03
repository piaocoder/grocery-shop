#coding:utf-8
def decorator(func):
    '''装饰器无参，函数无参'''
    print '类别1：'
    return func

@decorator
def perfect():
    print 'perfect man'
print '=========================='
# 等价于perfect=decorator(perfect), perfect()
perfect()
print '==========================end'
print 

def decorator1(func):
    '''装饰器无参，函数有参'''
    print '类别2：'
    def inner_func(*args, **kwargs):
        '''注意args、kwargs和外层函数没有任何关系'''
        print '%s begin:'%(func.__name__)
        func(*args, **kwargs)
        print '%s end:'%(func.__name__)
    return inner_func
@decorator1
def perfect1(name):
    print 'perfect man who\'s name is {0}'.format(name)
print '=========================='
# 等价于perfect=decorator1(perfect), perfect('bifeng')
perfect1('bifeng')
print '==========================end'
print 


def decorator2(decorate_args):
    '''装饰器有参，函数无参'''
    print '类别2：'
    def newDecorator(func):
        print '装饰器参数为：', decorate_args
        return func
    return newDecorator
@decorator2('-type 2 args-')
def perfect2():
    print 'perfect man'
print '=========================='
# 等价于perfect = decorator2('-type 2 args-')(perfect), perfect()
perfect2()
print '==========================end'
print 


def decorator3(decorate_args):
    '''装饰器有参，函数有参'''
    print '类别3：'
    def newDecorator(func):
        print '装饰器参数为：',decorate_args 
        def inner_func(*args, **kwargs):
            func(*args, **kwargs)
        return inner_func
    return newDecorator
@decorator3('-type 3 args-')
def perfect3(name):
    print 'perfect man who\'s name is {0}'.format(name)
print '=========================='
# 等价于perfect = decorator2('-type 2 args-')(perfect), perfect('bifeng')
perfect3('bifeng')
print '==========================end'
print 
