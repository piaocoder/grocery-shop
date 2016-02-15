#!/usr/bin/env python
#coding:utf-8
##
# @file bucketSort.py
# @brief    bucket sort simple test.
#       分析：
#           1，桶本身就已经是具备顺序的一个个集合
#           2，本质上，这是一种非比较类-线性时间-排序
#           3，物以类聚、人以群分，社会分层始终存在，左与右的选择
#           4，缺点：浪费空间，桶的数量
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def bucketSort(list1, bucket_num):
    """bucketSort:按照十位数进行桶排序，仅仅打印，不进行真正的结果返回

    :param list1:source list1
    :param bucket_num:bucket numbers
    """
    print '原始桶：'
    for value in list1:
        print value,
    print

    print '排序后的桶：'
    for i in xrange(10):
        for value in list1:
            if (value / 10) % 10 == i:
                print value,
    print

if __name__ == '__main__':
    list1 = [25353, 535, 53, 5, 696, 2953, 502, 55, 332, 222]
    bucketSort(list1, 10)
