#coding:utf-job
'''
    1，dfs--递归遍历，traversed recursively
    2，利用os.walk打印输出某一个指定目录下的所有文件
'''
import os

def recursePath(path):
    '''
    本身不会对path进行绝对值化，
    如果传入相对路径，输出为相对路径
    @rootpath: 整个path的起始根路径
    @dirnames：所有的目录项
    @filenames：所有的文件项
    函数walk本身逐级遍历，一层层进入
    '''
    for rootpath, dirnames, filenames in os.walk(path):
        print rootpath + "/"
        for memo in dirnames:
            print memo + "/"

        for memo in filenames:
            print memo


if __name__ == '__main__':
    '''main'''
    recursePath('../webOperator')
