def print_call(fn):
    ''' 
    函数指针或者函数的wrap使用
    '''
    def fn_wrap(*args, **kwargs):
        '''
        注意这里的args、kwargs其实和外层封装函数没有任何关系
        '''
        print "Calling %s with arguments: \n\targs: %s\n\tkwargs:%s"%(fn.__name__, args, kwargs)
        retval = fn(*args, **kwargs)
        print "%s returning '%s'" %(fn.func_name, retval)
        return retval
    # 函数名的赋值操作，多个指针指向同一个全局变量（函数名）
    fn_wrap.func_name = fn.func_name
    return fn_wrap

def bifeng_add(name, age='26'):
    print "Bifeng's name:%s, age:%s"%(name, age)
    return age

func1 = print_call(bifeng_add)
func1('20')
