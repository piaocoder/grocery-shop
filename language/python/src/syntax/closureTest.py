#coding:utf-8
'''
    closure闭包测试
'''

#def makeInc(x):
#    z = [3]
#    print "ID(x):{0}, ID(z):{1}".format(id(x), id(z))
#    def inc(y):
#        # 在函数inc中，x是闭合的，并关联
#        return x+y, "Closure(z):id(z)-", id(z)
#    # 返回动态的inc函数
#    return inc
#
## 获取动态函数实例1
#inc5 = makeInc(5)
## 获取动态函数的对象实例2
#inc10 = makeInc(10)
#
## 打印__closure__中的值，预测值为：
##   z的id是一样的，都引用了同一块内存值?（作用域变为global，可以通过co_globals查看）
##   ---->出现边界效应
##   
#print "Inc5:"
#print "Value:", inc5.__closure__[0].cell_contents, "  ", inc5.__closure__[1].cell_contents
#print "Id:", id(inc5.__closure__[0].cell_contents),"  ",  id(inc5.__closure__[1].cell_contents)
#print "Inc10:"
#print "Value:", inc10.__closure__[0].cell_contents,"  ",  inc10.__closure__[1].cell_contents
#print "Id:", id(inc10.__closure__[0].cell_contents),"  ",  id(inc10.__closure__[1].cell_contents)

def makeInc(x):
    z = 3
    print "ID(x):{0}, ID(z):{1}".format(id(x), id(z))
    def inc(y):
        # 在函数inc中，x是闭合的，并关联
        return x+y, "Closure(z):id(z)-", id(z)
    # 返回动态的inc函数
    return inc

# 获取动态函数实例1
inc5 = makeInc(5)
# 获取动态函数的对象实例2
inc10 = makeInc(10)

# 打印__closure__中的值，预测值为：
#   z的id是一样的，都引用了同一块内存值（作用域变为global，可以通过co_globals查看）
#   
print "Inc5:"
print "Value:", inc5.__closure__[0].cell_contents, "  ", inc5.__closure__[1].cell_contents
print "Id:", id(inc5.__closure__[0].cell_contents),"  ",  id(inc5.__closure__[1].cell_contents)
print "Inc10:"
print "Value:", inc10.__closure__[0].cell_contents,"  ",  inc10.__closure__[1].cell_contents
print "Id:", id(inc10.__closure__[0].cell_contents),"  ",  id(inc10.__closure__[1].cell_contents)



