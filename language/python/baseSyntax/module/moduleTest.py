#coding:utf-job
'''
    尝试以python -m module来执行python模块，并非以脚本形式执行；
    Searches sys.path for the named module and runs the corresponding .py file as a script
'''

if __name__ == '__main__':
    print '当前__name__为__main__脚本形式'
else:
    print '模块导入模式'
