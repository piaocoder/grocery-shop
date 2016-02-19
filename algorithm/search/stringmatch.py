#!/usr/bin/env python
#coding:utf-8
##
# @file stringmatch.py
# @brief    Searching for Patterns
# @author unlessbamboo
# @version 1.0
# @date 2016-02-18
import hashlib


def searchSimple(source, pat):
    """searchSimple:朴素匹配算法
       介绍：
           在每一个字符处进行匹配验证操作，
           验证次数为：n-m
       时间：
           O((n-m+1)*m)

    :param source:
    :param pat:
    """
    slen = len(source)
    plen = len(pat)

    for i in xrange(slen - plen + 1):
        for j in xrange(plen):
            if source[i + j] != pat[j]:
                break
        j += 1
        if j == plen:
            print "Pattern found at index " + str(i)
            break


def searchRabinKarp(source, pat):
    """searchRabinKarp:Rabin Karp算法
        分析：
            对朴素算法的一种改进，使用hash算法
            对某一个字串求取hash值，根据hash值来
            判断两个子串是否相等，从而加快的匹配速度

        步骤：
            1,pattern串长patlen, source串长为slen
            2,获取pattern的hash值phash
            3,遍历source，对于任意字串sch:
                计算hash值，schhash
                比较phash == schhash?
                    相等：使用朴素算法进行精确匹配
                    不相等：导演，下一个，不合格
            时间复杂度：
                O((N-M+1)*M),可能达到O(N+M)

        优化：
            1，构造hash表
            2，将每一个hash存储到对应的hash表中（拉链表存储）
            3，从而实现快速的检索（O(1)）
            4，一旦查找到对应的字符串：
                遍历链表，匹配字符串，O(n)

    :param source:
    :param pat:
    """
    patLen = len(pat)
    sourceLen = len(source)

    phash = hashlib.md5(pat).hexdigest()

    # Slide the pattern over text one by one
    for i in xrange(sourceLen - patLen + 1):
        # source hash
        thash = hashlib.md5(source[:i + patLen]).hexdigest()
        if phash == thash:
            # Check for characters one by one
            for j in xrange(patLen):
                if source[i + j] != pat[j]:
                    break
            j += 1
            if j == patLen:
                print "Pattern found at index " + str(i)
                break


def computeLps(pat, lps):
    """computeLps:计算pat的lps部分匹配表
        前续知识：
            前缀：除最后一个字符之外，字符串的所有头部组合
            后缀：除第一个字符之外，字符串的所有头部组合
            例如：
                abcd前缀：abc ab a
                abcd后缀：bcd cd d
        分析：
           1，部分匹配值 = 找出前缀和后缀的最长的共有元素长度（lps）
           2，部分匹配实质（kmp）：
                字符串头部和尾部存在重复，即字符串的部分匹配不为空；
                在搜索词移动时，就可以根据lps来快速的移动

        例子：
            abcdabd为例，每一个字串对应的lps-value：
                a       None                None            0
                ab      a                   b               0
                abc     ab,a                bc,c            0
                abcd    abc,ab,a            bcd,cd,d        0
                abcda   abcd,abc,ab,a       bcda,cda,da,a   1
                abcdab  ..,ab,a             ..,ab,b         2
                abcdabd ..,abc,ab,a         ..,abd,bd,d     0
        PS:
            前面一个子串存在相同的lps(k)，则后面的就可能+1，当然有可能为：
                k-1 ----相同的连续串，团结就是力量
                k-2 ----相同的连续串，团结就是力量
                ...
                0 ----逆水行舟，不进则死，退一步就是万丈深渊

    :param pat:
    :param lps:
    """
    # 初始值设置为0
    lps[0] = 0
    patLen = len(pat)

    # 假设前面已经匹配了，不管假匹配（0），或者真匹配
    i = 1
    klen = 0
    while i < patLen:
        if pat[i] == pat[klen]:
            klen += 1
            lps[i] = klen
            i += 1
        else:
            if klen:
                klen = lps[klen - 1]
            else:
                lps[klen] = 0
                i += 1


def searchKmp(source, pat):
    """searchKmp:kmp搜索算法
        分析：
            步骤：
                1，pat[patindex] == source[sindex]时，patindex++,sindex++
                    判断patindex == plen：
                        相等——匹配成功
                        不相等——继续下一个匹配
                2，不匹配时：
                    移动位数 = 已经匹配字符数 - 当前匹配子串对应的lps-value
                    当前匹配字串：lsp[patindex - 1]

            例如：
                模式串abcdabuu的next值为：
                    0 0 0 0 1 2 0 0
                原始串为
                    abcdabyyxxxxy
                当匹配到：
                    abcdabyyxxxxy
                    abcdabu----
                    发现u和y不匹配，获取匹配字符串的next值，即
                    pat[patindex-1]的值 == 2

    :param source:
    :param pat:
    """
    plen = len(pat)
    slen = len(source)
    lps = [0] * plen
    patindex = 0
    sindex = 0

    # 计算lps-value
    computeLps(pat, lps)

    # match
    while sindex < slen:
        if pat[patindex] == source[sindex]:
            patindex += 1
            sindex += 1
            if patindex == plen:
                break
        else:
            patindex = lps[patindex - 1]

    if patindex == plen:
        print "Pattern found at index " + str(sindex - patindex)
    else:
        print "Pattern not found."


def searchBoyerMoore(source, pat):
    """searchBoyerMoore(BM算法):grep使用，快于kmp3~5倍

    :param source:
    :param pat:
    """
    pass


def searchSunday(source, pat):
    """searchSunday:优于kmp，易于理解

    :param source:
    :param pat:
    """
    pass


if __name__ == '__main__':
    source = "GEEKS FOR GEEKS"
    pat = "GEEK"
    # searchRabinKarp(source, pat)
    searchSimple(source, pat)
