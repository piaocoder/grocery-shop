#coding:utf-8
#!/usr/bin/python
import logging

def console():
    '''默认级别为：Warning'''
    logging.debug('This is a test message of default print.')
    logging.info('This is a test message of default print.')
    logging.warning('This is a test message of default print.')

def file():
    ############################################
    # 如果添加该行，则无法输出到文件中
    logging.warning('This is a test message of default print.')
    #############################################

    logging.basicConfig(level=logging.DEBUG, \
            format=('%(asctime)s %(filename)s[line:%(lineno)d]'\
                '%(levelname)s %(message)s'),\
            filename = './test.log', \
            filemode = 'w')
    logging.debug('This is a test message of filename print.')
    logging.error('This is a test message of filename print.')

def fileHandle():
    ############################################
    '''如果添加该行，则无法输出到文件中，此时查看源码，可以发现:
        if len(root.handlers) == 0:
            ...(未执行) 
    '''
    logging.warning('This is a test message of default print.')
    #############################################

    logging.basicConfig(level=logging.DEBUG, \
            format=('%(asctime)s %(filename)s[line:%(lineno)d]'\
                '%(levelname)s %(message)s'),\
            filename = './test.log', \
            filemode = 'w')
    logging.debug('This is a test message of filename print.')
    logging.error('This is a test message of filename print.')

def streamHandle():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    format = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(format)
    logging.getLogger('').addHandler(console)

    logging.error('This ia a test message for streamHandle.')

if __name__ == '__main__':
    #console()
    #file()
    #fileHandle()
    streamHandle()
