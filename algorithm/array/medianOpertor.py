#!/usr/bin/env python
#coding:utf-8


def findMedianSortedArrays(list1, list2):
    """findMedianSortedArrays
        https://leetcode.com/discuss/15790/
            share-my-o-log-min-m-n-solution-with-explanation
        1，what is median?
            In statistics, the median is used for
            dividing a set into two equal length
            subsets, that one subset is always
            greater than the other.
        2，在使用二分法提取两个数组的median时，任意时刻必须保证如下条件：
                  left_part          |        right_part
            A[0], A[1], ..., A[i-1]  |  A[i], A[i+1], ..., A[m-1]
            B[0], B[1], ..., B[j-1]  |  B[j], B[j+1], ..., B[n-1]

            Ensure 1:
                len(left_part) == len(right_part);
                max(left_part) <= min(right_part);
                正常的二分法也是此种思路

            Ensure 2:
                i-1 - 0 + 1 + j-1 -0 + 1 == m-1 - i + 1 + n-1 - j + 1
                --> i + j == m - i + n - j (偶数);
                B[j-1] <= A[i] and A[i-1] <= B[j];
                可得出，对于任意的i：
                    j = (m+n+1)/2 - i;
                    B[j-1] <= A[i] and A[i-1] <= B[j]，此时条件成立

        3，edges value handle
            所有讨论前提为：j = (m+n+1)/2 - i
            if i == 0 or j == 0 or i==m or j == n:
                表示某一个数组已经是空了，无需进行验证，例如i==0，j==n，此时
                无需验证A[i-1] <= B[j]
            else
                B[j-1] <= A[i] and A[i-1] <= B[j]，成功分割

        4，use median loop, we will encounter only tree situations:
            situations 1:
                i == 0 or i == m or B[j-1] <= A[i]
                    and
                j == 0 or j == n or A[i-1] <= B[j]
                分割完毕，准备赋值退出
            situations 2:
                j > 0 and i < m and B[j-1] > A[i]:
                    此时需要递增i
            situations 3:
                i > 0 and j < n and A[i-1] > B[j]:
                    此时需要递减i

    :param list1:
    :param list2:
    """
    len1 = len(list1)
    len2 = len(list2)

    # ensure len1 < len2
    if len1 > len2:
        list1, list2, len1, len2 = list2, list1, len2, len1
    if len2 == 0:
        raise ValueError

    imin, imax, half_len = 0, len1, (len1 + len2 + 1) / 2
    while imin <= imax:
        i = (imin + imax) / 2
        j = half_len - i

        if j > 0 and i < len1 and list2[j - 1] > list1[i]:
            imin = i + 1
        elif i > 0 and j < len2 and list1[i - 1] > list2[j]:
            imin = i - 1
        else:
            # situations 1
            if i == 0:
                max_of_left = list2[j - 1]
            elif j == 0:
                max_of_left = list1[i - 1]
            else:
                max_of_left = max(list2[j - 1], list1[i - 1])

            # odd-even
            if (len1 + len2) % 2 == 1:
                return max_of_left
            else:
                if i == len1:
                    min_of_right = list2[j]
                elif j == len2:
                    min_of_right = list1[i]
                else:
                    min_of_right = max(list1[i], list2[j])
                return (max_of_left + min_of_right) / 2.0

if __name__ == '__main__':
    pass
