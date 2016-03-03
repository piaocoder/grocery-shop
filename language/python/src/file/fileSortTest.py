#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import stat

def sortdir(path, sort_cond = 'mtime',  sort_filter = None, reverse = True, abspath = True, onlyfn = True, postfix = None):
    '''
    sort dir by give condition & filter

    :param path: dir path
    :param sort_cond:
    ctime: create time
    mtime: last modify time
    atime: atime
    size: file size
    :param sort_filter:
    function to filter
    1: only file
    2: only dir
    3: both file and dir
    func: custom function
    :param reverse:
    if sort reversed
    :param abspath:
    if True, return list with absolute path of file
    or else, return relative
    :param onlyfn:
    if True, return [filename1, filename2, ....] at sort_cond
    else, return [(filename, os.stat(file), (), ...] at sort_cond

    :return:
    [(filename, os.stat(file), (), ...] at sort_cond
    '''

    # sort condition
    if sort_cond == "mtime":
        f_sort_cond = lambda e:e[1].st_mtime
    elif sort_cond == "ctime":
        f_sort_cond = lambda e:e[1].st_ctime
    elif sort_cond == "atime":
        f_sort_cond = lambda e:e[1].st_atime
    elif sort_cond == "size":
        f_sort_cond = lambda e:e[1].st_size
    else:
        f_sort_cond = lambda e:e[1].st_mtime

    # sort filter
    f_sf = None
    if sort_filter == None or sort_filter == 3:
        # None, file or directory
        f_sf = None
    elif type(sort_filter) == type(lambda x:x):
        # user defined function
        f_sf = sort_filter
    else:
        if sort_filter == 1:
            # common file 
            f_sf = lambda e: stat.S_ISDIR(e.st_mode) == 0
        elif sort_filter == 2:
            # directory
            f_sf = lambda e: stat.S_ISDIR(e.st_mode)
        else:
            f_sf = None

    # if onlyfn is True, return [filename1, filename2, ...]
    if onlyfn:
        return map(lambda e:e[0], __sortdir(path, f_sort_cond, f_sf, reverse, abspath, postfix))

    return __sortdir(path, f_sort_cond, f_sf, reverse, abspath, postfix)

def __sortdir(path, sort_cond, sort_filter, reverse, abspath, postfix):
    '''
    Sort a directory by sort_cond.
    '''
    fns = os.listdir(path)
    if not path.endswith('/'):
        path = path + '/'

    # map对于fns中的每个参数，调用函数f，函数式编程
    a_fns = map(lambda f: path+f, fns)
    sts = map(os.stat, a_fns)

    # zip接受一系列可迭代的对象作为参数，将对象中对应的元素打包成一个个
    # tuple元祖
    if abspath:
        res = zip(a_fns, sts)
    else:
        res = zip(fns, sts)

    n_res = []
    for e in res:
        if sort_filter != None and postfix != None:
            if postfix(e[0]) and sort_filter(e[1]):
                n_res.append(e)
        elif sort_filter != None and postfix == None:
            if sort_filter(e[1]):
                n_res.append(e)
        elif sort_filter == None and postfix != None:
            if postfix(e[0]):
                n_res.append(e)

    return sorted(n_res, key = sort_cond, reverse = reverse)

def removeOutDateFile(file_list, file_number):
    '''
    remove outdate file
    '''
    list_length = len(file_list)
    print list_length
    if file_number > list_length:
        return

    for index in range(file_number-1, list_length):
        os.remove(file_list[index])
        print file_list[index]

def fileFilter(filename):
    '''
    Filter of file.
    '''
    return filename.endswith(".info")

if __name__ == '__main__':
    '''
    Main
    '''
    file_list = sortdir('/home/temp/', postfix = fileFilter)  
    for element in file_list:
        print element
    #removeOutDateFile(file_list, 20)
