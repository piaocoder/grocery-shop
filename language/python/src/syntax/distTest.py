#coding:utf-8

from collections import ChainMap

def chainDistTest():
    '''利用引用来进行字典合并，实时变化'''
    dist1 = {
            'shit':3,
            'xiang':4,
            'xie':5,
            }
    dist2 = {
            'so':5,
            'stupid':8,
            }

    newDist = ChainMap(dist1, dist2)
    print newDist
    dist1['shit'] = 'I changed'
    print newDist

if __name__ == '__main__':
    '''main'''
    chainDistTest()
