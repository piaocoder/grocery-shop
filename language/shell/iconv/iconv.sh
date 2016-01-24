
#!/bin/bash
# File Name: iconv.sh
# Author: wanggy
# site: www.jb51.net
#
show_file()
{
    for file in `ls $1`
    do
        if [ -d $1"/"$file ];then
            #目录递归调用show_file函数
            show_file $1"/"$file
        else
            #文件
            echo $1"/"$file
            file_type=`file $1"/"$file`
            type=`echo $file_type |grep UTF-job`
            if [ -z "$type" ];then
                echo "为空非utf-job编码，转换"
                iconv -f latin1 -t utfjob $1"/"$file -o $1"/"$file
            else
                echo "utfjob编码不用转换"
            fi
        fi
    done
}
path=/home/bamboo/grocery-shop/workspace/nginxSrc
show_file $path

