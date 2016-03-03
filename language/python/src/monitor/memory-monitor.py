#!/usr/bin/env python
#coding:utf-8

import sys
from guppy import hpy

list1 = ['shite', 'gelgelgejge', 'xxxxx',
        'gejglejgeljg', 'iiiiiiiiiiiiiiii', 'xxxxxxxxxx',
        'bbbbbbbbbb', 'xxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxx',
        'vvvvvvvvvv', 'bbbbbbbbbbb', 'nnnnnnnnnnnnnn',
        'ccccccccccc', 'nnnnnnnn', 'mmmmmmmmmmmmmm',
        '........', 'rrrrrrrrrr', 'ttttttttttttttttt',
        ]

def index():
    global list1
    hp = hpy()
    hp.setrelheap()

    for i in list1:
        i

    h = hp.heap()
    print h
    print h.more

def item():
    global list1
    hp = hpy()
    hp.setrelheap()

    for i in range(len(list1)):
        list1[i]

    h = hp.heap()
    print h
    print h.more

if __name__ == '__main__':
    '''main'''
    if len(sys.argv) <= 1:
        exit(-1)
    if sys.argv[1] == 'index':
        index()
    else:
        item()
