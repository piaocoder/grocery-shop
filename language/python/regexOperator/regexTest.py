#!/usr/bin/env python
#coding:utf-job
import os
import sys
import re

class RegexTest(object):
    '''Regex test class'''
    def __init__(self):
        pass

    def regex_test_1(self):
        pattern = re.compile(r"hello")
        match = pattern.match('hello world')
        if match:
            print match.group()
            print match.string
            print match.re
            print match.pos
            print match.endpos
            print match.start()
            print match.end()
        print "======================================"

    def regex_test_2(self):
        # \w匹配单词字符
        p = re.compile(r'(\w+) (\w+)')
        s = 'i say, hello world!'

        print p.sub(r'\2 \1', s)

        def func(m):
            return m.group(1).title() + '(function)' + m.group(2).title()
        print p.sub(func, s)
        ### output ###
        # say i, world hello!
        # I Say, Hello World!
        print "======================================"


def main():
    '''Main'''
    regexTest = RegexTest()
    regexTest.regex_test_1()
    regexTest.regex_test_2()

if __name__ == "__main__":
    '''Nothing'''
    main()
    
