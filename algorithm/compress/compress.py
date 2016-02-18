#!/usr/bin/env python
#coding:utf-8
##
# @file compress.py
# @brief    字符串压缩算法介绍（不单独放在string中了，翅膀硬了）
# @author unlessbamboo
# @version 1.0
# @date 2016-02-17


def compressHash(str1):
    """compressHash:字典算法
        介绍：
            将高频词汇或者词汇组合hash，并以较小的特殊代码替换，
            从而达到压缩的目的
        使用场景
            专有名词较多的应用场景，例如某些游戏
        例子：
            00 == Chinese
            01 == China
            02 == people
            则压缩结果为：
                I am a 00 02, I am from 01. So what?

    :param str1:
    """
    pass


def compressFixedBitLength(str1):
    """compressFixedBitLength:固定位长算法
        介绍：
            按照统计学思想，大部分的字符都是使用低位编码，高位编码一般
            为特殊字符（utf8好像不是），尽量的提取最少位进行压缩
        例子：
            1,2,3,4,5,6,7,8,9
            原本二进制位：
            0x01,0x02,0x03,0x04,...,0x09
            压缩为：
            0001,0010,0011,...,1001
            最后组合为：
            0x12,0x34,0x56,0x78,0x9?
        最终达到压缩效果

    :param str1:
    """
    pass


def compressRle(str1):
    """compressRle:变长RLE算法
        介绍：
            高适应性的编码，根据文本的不同情况选择不同的编码变体，
            从而产生巨大的压缩比率
            变体1：
                重复次数+字符
                例如：
                    AAABBBCCCCDDDD变为3A 3B 4C 4D
            变体2：
                特殊字符 + 重复次数 + 字符
                （避免文本中存在整数的情况）
                例如：
                    AAABBBCCCCBDDDD变为B B3A BBB B4C B B4D
            变体3：
                将文本的每一个字节分组成块，每一个字符最多重复127次（看后面），
                格式：
                    特殊字节 + 块
                    如果特殊字节第7位（最高BIT位）置1：
                        剩下的7位表示后面字符重复次数（127次的由来），例如：
                        AAAAA变为85A，10000101 A
                    如果特殊字节第7为未被置1：
                        剩下7位表示后面没有被压缩的字符数量，例如：
                        BCDE变为4BCDE，00000100 BCDE
            其他变体
        应用场景：
            winzip winrar中使用

    :param str1:
    """
    pass


def compressLz77(str1):
    """compressLz77:LZ77算法
        介绍：
            Silding window(动态窗口)：
                0K-64K，一般为4K
                历史缓冲器，存入输入流中的前面n个字节的信息（这个样板很重要啊）

                PS:SW也是一直处于往前移动状态，只不过其值一直都是原始字符串

            Read Ahead Buffer(预读缓冲器)：
                一般为0-258Byte
                读取后面的m个字节信息，和SW进行匹配（保证匹配长度大于编码器规定）：
                    1,如果匹配（KMP），返回<off, len, c>
                        off：SW中匹配字符串相对窗口边界偏移量
                        len：匹配长度
                        c：RAB中的下一个字符，一般原样输入，没有匹配成功
                        之后SW向后移动len + 1字符，重新开始
                    2,如果不匹配或者长度过小，返回<0, 0, c>
                        窗口下后移动1字符，重新开始

        例如：
            最小匹配长度为2
            文本：abcdb bccaa abaea aabae e
            SW（长度为10）：abcdb bccaa
            待处理文本(长度为10）：abaea aabae
            ===================
            匹配ab，返回<0, 2, a>，SW和RAB向前移动3个字符
            SB：dbbcc aaaba
            RAB：eaaab aee
            ==================
            未匹配，返回<0, 0, e>，前移动1字符
            SB：bbcca aabae
            RAB：aaaba ee
            =================
            匹配，返回<4,6,e>

    :param str1:
    """
    pass


if __name__ == '__main__':
    str1 = "I am a Chinese people, I am from China. So what?"
    print '原始列表：'
    print str1
    print '排序后的列表：'
    print str1
